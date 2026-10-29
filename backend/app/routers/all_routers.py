"""Matching, Deliveries, Organizations, Waste, Analytics routers"""
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
from app.models.db_models import (
    get_db, User, Organization, FoodBatch, DonationMatch,
    Delivery, RecipientRequirement, WasteBatch, AuditLog,
    BatchStatus, MatchStatus, DeliveryStatus, WasteStatus
)
from app.auth import get_current_user, require_roles
from app.services.freshguard import match_recipients

# ─── Organizations ────────────────────────────────────────────────────────────
orgs_router = APIRouter(prefix="/organizations", tags=["Organizations"])

class OrgUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    service_area_radius_km: Optional[float] = None

def _org_out(o: Organization):
    return {
        "id": o.id, "name": o.name, "organization_type": o.organization_type,
        "address": o.address, "latitude": o.latitude, "longitude": o.longitude,
        "service_area_radius_km": o.service_area_radius_km,
        "verification_status": o.verification_status,
        "created_at": o.created_at.isoformat() if o.created_at else None,
        "verified_at": o.verified_at.isoformat() if o.verified_at else None,
    }

@orgs_router.get("/")
def list_orgs(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    orgs = db.query(Organization).all()
    return [_org_out(o) for o in orgs]

@orgs_router.get("/{org_id}")
def get_org(org_id: str, db: Session = Depends(get_db)):
    org = db.query(Organization).filter(Organization.id == org_id).first()
    if not org:
        raise HTTPException(404, "Organization not found")
    return _org_out(org)

@orgs_router.patch("/{org_id}")
def update_org(org_id: str, req: OrgUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    org = db.query(Organization).filter(Organization.id == org_id).first()
    if not org:
        raise HTTPException(404, "Organization not found")
    for field, val in req.dict(exclude_none=True).items():
        setattr(org, field, val)
    db.commit()
    return _org_out(org)

@orgs_router.post("/{org_id}/verify")
def verify_org(org_id: str, current_user: User = Depends(require_roles("ADMIN")), db: Session = Depends(get_db)):
    org = db.query(Organization).filter(Organization.id == org_id).first()
    if not org:
        raise HTTPException(404, "Organization not found")
    org.verification_status = "VERIFIED"
    org.verified_at = datetime.utcnow()
    org.verified_by = current_user.id
    db.commit()
    return _org_out(org)


# ─── Recipient Requirements ───────────────────────────────────────────────────
reqs_router = APIRouter(prefix="/recipient-requirements", tags=["Recipient Requirements"])

class ReqCreate(BaseModel):
    food_category: str
    quantity_needed_kg: float
    capacity_kg: float
    available_from: Optional[str] = None
    available_until: Optional[str] = None
    dietary_constraints: Optional[list] = []

@reqs_router.post("/")
def create_req(req: ReqCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not current_user.organization_id:
        raise HTTPException(400, "Must belong to an organization")
    rr = RecipientRequirement(
        recipient_id=current_user.organization_id,
        food_category=req.food_category,
        quantity_needed_kg=req.quantity_needed_kg,
        capacity_kg=req.capacity_kg,
        available_from=datetime.fromisoformat(req.available_from) if req.available_from else None,
        available_until=datetime.fromisoformat(req.available_until) if req.available_until else None,
        dietary_constraints=req.dietary_constraints or [],
    )
    db.add(rr)
    db.commit()
    db.refresh(rr)
    return {"id": rr.id, "food_category": rr.food_category, "status": rr.status}

@reqs_router.get("/")
def list_reqs(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    reqs = db.query(RecipientRequirement).filter(RecipientRequirement.status == "ACTIVE").all()
    return [{"id": r.id, "food_category": r.food_category, "quantity_needed_kg": r.quantity_needed_kg,
             "capacity_kg": r.capacity_kg, "recipient_id": r.recipient_id,
             "recipient_name": r.recipient.name if r.recipient else None} for r in reqs]


# ─── Matching ─────────────────────────────────────────────────────────────────
match_router = APIRouter(prefix="/matches", tags=["Matching"])

def _match_out(m: DonationMatch):
    return {
        "id": m.id, "batch_id": m.batch_id, "recipient_id": m.recipient_id,
        "offered_quantity_kg": m.offered_quantity_kg,
        "accepted_quantity_kg": m.accepted_quantity_kg,
        "estimated_distance_km": m.estimated_distance_km,
        "match_score": m.match_score, "status": m.status,
        "created_at": m.created_at.isoformat() if m.created_at else None,
        "recipient_name": m.recipient.name if m.recipient else None,
        "batch_food": m.batch.food_category if m.batch else None,
    }

@match_router.post("/run-matching/{batch_id}")
def run_matching(batch_id: str, current_user: User = Depends(require_roles("ADMIN", "ASSESSOR")), db: Session = Depends(get_db)):
    batch = db.query(FoodBatch).filter(FoodBatch.id == batch_id, FoodBatch.status == BatchStatus.MATCHING).first()
    if not batch:
        raise HTTPException(404, "Batch not found or not in MATCHING state")

    reqs = db.query(RecipientRequirement).filter(RecipientRequirement.status == "ACTIVE").all()
    donor = db.query(Organization).filter(Organization.id == batch.donor_id).first()

    scored = match_recipients(batch, reqs, donor.latitude if donor else None, donor.longitude if donor else None)
    created_matches = []

    for s in scored[:3]:  # Top 3 matches
        existing = db.query(DonationMatch).filter(
            DonationMatch.batch_id == batch_id,
            DonationMatch.recipient_id == s["organization"].id if s["organization"] else None,
            DonationMatch.status == MatchStatus.OFFERED
        ).first()
        if not existing and s["organization"]:
            m = DonationMatch(
                batch_id=batch_id,
                recipient_id=s["organization"].id,
                offered_quantity_kg=batch.quantity_kg,
                estimated_distance_km=s["estimated_distance_km"],
                match_score=s["match_score"],
                status=MatchStatus.OFFERED
            )
            db.add(m)
            created_matches.append(m)

    batch.status = BatchStatus.MATCHED
    db.commit()
    return {"matches_created": len(created_matches), "top_matches": [_match_out(m) for m in created_matches]}

@match_router.get("/")
def list_matches(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    q = db.query(DonationMatch)
    if current_user.role == "RECIPIENT" and current_user.organization_id:
        q = q.filter(DonationMatch.recipient_id == current_user.organization_id)
    elif current_user.role == "DONOR" and current_user.organization_id:
        batch_ids = [b.id for b in db.query(FoodBatch.id).filter(FoodBatch.donor_id == current_user.organization_id)]
        q = q.filter(DonationMatch.batch_id.in_(batch_ids))
    return [_match_out(m) for m in q.order_by(DonationMatch.created_at.desc()).all()]

@match_router.post("/{match_id}/accept")
def accept_match(match_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    m = db.query(DonationMatch).filter(DonationMatch.id == match_id).first()
    if not m:
        raise HTTPException(404, "Match not found")
    m.status = MatchStatus.ACCEPTED
    m.accepted_quantity_kg = m.offered_quantity_kg
    m.responded_at = datetime.utcnow()
    # Create delivery record
    delivery = Delivery(
        match_id=match_id,
        status=DeliveryStatus.SCHEDULED,
        scheduled_pickup=datetime.utcnow(),
        dispatched_quantity_kg=m.accepted_quantity_kg
    )
    db.add(delivery)
    if m.batch:
        m.batch.status = BatchStatus.PICKUP_SCHEDULED
    db.commit()
    return {"status": "ACCEPTED", "delivery_id": delivery.id}

@match_router.post("/{match_id}/decline")
def decline_match(match_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    m = db.query(DonationMatch).filter(DonationMatch.id == match_id).first()
    if not m:
        raise HTTPException(404, "Match not found")
    m.status = MatchStatus.DECLINED
    m.responded_at = datetime.utcnow()
    db.commit()
    return {"status": "DECLINED"}


# ─── Deliveries ───────────────────────────────────────────────────────────────
delivery_router = APIRouter(prefix="/deliveries", tags=["Deliveries"])

@delivery_router.get("/")
def list_deliveries(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    from sqlalchemy.orm import joinedload
    deliveries = (
        db.query(Delivery)
        .options(
            joinedload(Delivery.match).joinedload(DonationMatch.batch).joinedload(FoodBatch.donor),
            joinedload(Delivery.match).joinedload(DonationMatch.recipient),
        )
        .order_by(Delivery.created_at.desc())
        .all()
    )
    out = []
    for d in deliveries:
        match = d.match
        batch = match.batch if match else None
        donor = batch.donor if batch else None
        recipient = match.recipient if match else None
        out.append({
            "id": d.id,
            "match_id": d.match_id,
            "status": d.status,
            "food_category": batch.food_category if batch else "Surplus Food",
            "quantity_kg": (
                d.delivered_quantity_kg
                or d.dispatched_quantity_kg
                or (match.accepted_quantity_kg if match else None)
                or (batch.quantity_kg if batch else 0)
            ),
            "donor_name": donor.name if donor else "Donor Kitchen",
            "donor_address": donor.address if donor else "Pune, Maharashtra",
            "recipient_name": recipient.name if recipient else "Community Shelter",
            "recipient_address": recipient.address if recipient else "Shelter Location",
            "distance_km": match.estimated_distance_km if match else 4.2,
            "scheduled_pickup": d.scheduled_pickup.isoformat() if d.scheduled_pickup else None,
            "actual_pickup": d.actual_pickup.isoformat() if d.actual_pickup else None,
            "actual_delivery": d.actual_delivery.isoformat() if d.actual_delivery else None,
            "created_at": d.created_at.isoformat() if d.created_at else None,
        })
    return out

@delivery_router.post("/{delivery_id}/pickup")
def record_pickup(delivery_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    d = db.query(Delivery).filter(Delivery.id == delivery_id).first()
    if not d:
        raise HTTPException(404, "Delivery not found")
    d.actual_pickup = datetime.utcnow()
    d.status = DeliveryStatus.IN_TRANSIT
    if d.match and d.match.batch:
        d.match.batch.status = BatchStatus.IN_TRANSIT
    db.commit()
    return {"status": "IN_TRANSIT"}

class ConfirmDelivery(BaseModel):
    delivered_quantity_kg: float
    notes: Optional[str] = ""

@delivery_router.post("/{delivery_id}/confirm")
def confirm_delivery(delivery_id: str, req: ConfirmDelivery, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    d = db.query(Delivery).filter(Delivery.id == delivery_id).first()
    if not d:
        raise HTTPException(404, "Delivery not found")
    if d.actual_delivery:  # Idempotent
        return {"status": "DELIVERED", "already_confirmed": True}
    d.delivered_quantity_kg = req.delivered_quantity_kg
    d.actual_delivery = datetime.utcnow()
    d.status = DeliveryStatus.DELIVERED
    d.recipient_confirmation = {"confirmed_at": datetime.utcnow().isoformat(), "notes": req.notes}
    # Update match status
    if d.match:
        d.match.status = MatchStatus.COMPLETED
        # Update batch status
        if d.match.batch:
            d.match.batch.status = BatchStatus.DELIVERED
    db.commit()
    return {"status": "DELIVERED"}


# ─── Waste Management ─────────────────────────────────────────────────────────
waste_router = APIRouter(prefix="/waste-batches", tags=["Waste Management"])

WASTE_CATEGORIES = ["Fruit Scraps", "Vegetable Prep Waste", "Cooked Food (Rejected)",
                    "Plate Waste", "Raw Ingredient (Spoiled)", "Coffee Grounds", "Other Biodegradable"]

class WasteCreate(BaseModel):
    waste_category: str
    quantity_kg: float
    contamination_status: Optional[str] = "UNKNOWN"
    contamination_details: Optional[str] = ""

class ProcessorConfirm(BaseModel):
    received_quantity_kg: float
    processing_method: Optional[str] = "COMPOSTING"
    compost_output_kg: Optional[float] = None
    biogas_output_m3: Optional[float] = None

@waste_router.get("/categories")
def waste_categories():
    return WASTE_CATEGORIES

@waste_router.post("/")
def create_waste(req: WasteCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not current_user.organization_id:
        raise HTTPException(400, "Must belong to an organization")
    w = WasteBatch(
        donor_id=current_user.organization_id,
        waste_category=req.waste_category,
        quantity_kg=req.quantity_kg,
        contamination_status=req.contamination_status,
        contamination_details=req.contamination_details,
    )
    db.add(w)
    db.commit()
    db.refresh(w)
    return {"id": w.id, "status": w.status, "waste_category": w.waste_category, "quantity_kg": w.quantity_kg}

@waste_router.get("/")
def list_waste(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    q = db.query(WasteBatch)
    if current_user.role == "DONOR" and current_user.organization_id:
        q = q.filter(WasteBatch.donor_id == current_user.organization_id)
    elif current_user.role == "PROCESSOR" and current_user.organization_id:
        q = q.filter(WasteBatch.processor_id == current_user.organization_id)
    batches = q.order_by(WasteBatch.created_at.desc()).all()
    return [{"id": w.id, "waste_category": w.waste_category, "quantity_kg": w.quantity_kg,
             "contamination_status": w.contamination_status, "status": w.status,
             "processor_id": w.processor_id,
             "received_quantity_kg": w.received_quantity_kg,
             "processing_outcome": w.processing_outcome} for w in batches]

@waste_router.post("/{waste_id}/assign-processor/{processor_id}")
def assign_processor(waste_id: str, processor_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    w = db.query(WasteBatch).filter(WasteBatch.id == waste_id).first()
    if not w:
        raise HTTPException(404, "Waste batch not found")
    proc = db.query(Organization).filter(Organization.id == processor_id, Organization.organization_type == "PROCESSOR").first()
    if not proc:
        raise HTTPException(404, "Processor not found")
    w.processor_id = processor_id
    w.status = WasteStatus.SCHEDULED
    db.commit()
    return {"status": "SCHEDULED", "processor_id": processor_id, "processor_name": proc.name}

@waste_router.post("/{waste_id}/confirm-receipt")
def confirm_receipt(waste_id: str, req: ProcessorConfirm, current_user: User = Depends(require_roles("PROCESSOR", "ADMIN")), db: Session = Depends(get_db)):
    w = db.query(WasteBatch).filter(WasteBatch.id == waste_id).first()
    if not w:
        raise HTTPException(404, "Waste batch not found")
    w.received_quantity_kg = req.received_quantity_kg
    w.status = WasteStatus.RECEIVED
    db.commit()
    return {"status": "RECEIVED", "received_quantity_kg": req.received_quantity_kg}

@waste_router.post("/{waste_id}/confirm-processing")
def confirm_processing(waste_id: str, req: ProcessorConfirm, current_user: User = Depends(require_roles("PROCESSOR", "ADMIN")), db: Session = Depends(get_db)):
    w = db.query(WasteBatch).filter(WasteBatch.id == waste_id).first()
    if not w:
        raise HTTPException(404, "Waste batch not found")
    w.status = WasteStatus.PROCESSED
    w.received_quantity_kg = req.received_quantity_kg
    w.processing_outcome = {
        "method": req.processing_method,
        "compost_output_kg": req.compost_output_kg,
        "biogas_output_m3": req.biogas_output_m3,
        "confirmed_at": datetime.utcnow().isoformat()
    }
    db.commit()
    return {"status": "PROCESSED", "outcome": w.processing_outcome}


# ─── Analytics ────────────────────────────────────────────────────────────────
analytics_router = APIRouter(prefix="/analytics", tags=["Analytics"])

@analytics_router.get("/summary")
def summary(db: Session = Depends(get_db)):
    total_reported = db.query(func.sum(FoodBatch.quantity_kg)).scalar() or 0
    total_delivered = db.query(func.sum(Delivery.delivered_quantity_kg)).filter(
        Delivery.status == DeliveryStatus.DELIVERED).scalar() or 0
    total_approved = db.query(func.count(FoodBatch.id)).filter(
        FoodBatch.status.in_(["APPROVED", "MATCHING", "MATCHED", "PICKUP_SCHEDULED", "IN_TRANSIT", "DELIVERED"])).scalar() or 0
    total_rejected = db.query(func.count(FoodBatch.id)).filter(FoodBatch.status == BatchStatus.REJECTED).scalar() or 0
    total_waste_reported = db.query(func.sum(WasteBatch.quantity_kg)).scalar() or 0
    total_waste_processed = db.query(func.sum(WasteBatch.received_quantity_kg)).filter(
        WasteBatch.status.in_(["RECEIVED", "PROCESSED"])).scalar() or 0
    batches_by_status = {}
    for b in db.query(FoodBatch.status, func.count(FoodBatch.id)).group_by(FoodBatch.status).all():
        batches_by_status[b[0]] = b[1]

    return {
        "food_recovery": {
            "total_reported_kg": round(total_reported, 2),
            "total_approved_count": total_approved,
            "total_delivered_kg": round(total_delivered, 2),
            "total_rejected_count": total_rejected,
            "estimated_meals_served": round(total_delivered * 4),  # ~250g per meal
            "batches_by_status": batches_by_status,
        },
        "waste_management": {
            "total_waste_reported_kg": round(total_waste_reported, 2),
            "total_waste_diverted_kg": round(total_waste_processed, 2),
        },
        "organizations": {
            "total": db.query(func.count(Organization.id)).scalar() or 0,
            "verified": db.query(func.count(Organization.id)).filter(Organization.verification_status == "VERIFIED").scalar() or 0,
        },
        "note": "Delivered quantities are from recipient-confirmed records only."
    }

@analytics_router.get("/food-recovery")
def food_recovery(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    deliveries = db.query(Delivery).filter(Delivery.status == DeliveryStatus.DELIVERED).all()
    return {
        "completed_deliveries": len(deliveries),
        "total_delivered_kg": sum(d.delivered_quantity_kg or 0 for d in deliveries),
        "deliveries": [{"id": d.id, "delivered_kg": d.delivered_quantity_kg,
                        "date": d.actual_delivery.isoformat() if d.actual_delivery else None} for d in deliveries]
    }

@analytics_router.get("/waste-processing")
def waste_processing(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    processed = db.query(WasteBatch).filter(WasteBatch.status == WasteStatus.PROCESSED).all()
    return {
        "total_processed_batches": len(processed),
        "total_confirmed_kg": sum(w.received_quantity_kg or 0 for w in processed),
        "batches": [{"id": w.id, "category": w.waste_category,
                     "received_kg": w.received_quantity_kg,
                     "outcome": w.processing_outcome} for w in processed]
    }

@analytics_router.get("/admin")
def admin_analytics(current_user: User = Depends(require_roles("ADMIN")), db: Session = Depends(get_db)):
    pending_assessments = db.query(func.count(FoodBatch.id)).filter(
        FoodBatch.status == BatchStatus.ASSESSMENT_REQUIRED).scalar() or 0
    pending_verifications = db.query(func.count(Organization.id)).filter(
        Organization.verification_status == "PENDING").scalar() or 0
    recent_logs = db.query(AuditLog).order_by(AuditLog.created_at.desc()).limit(20).all()
    return {
        "pending_assessments": pending_assessments,
        "pending_org_verifications": pending_verifications,
        "recent_audit_logs": [
            {"action": l.action, "entity_type": l.entity_type,
             "entity_id": l.entity_id, "created_at": l.created_at.isoformat()}
            for l in recent_logs
        ]
    }
