"""Food batches router — full CRUD + AI assessment + approve/reject"""
import os, shutil
from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.models.db_models import (
    get_db, User, FoodBatch, ModelAssessment, FoodAssessment,
    AuditLog, Organization, BatchStatus
)
from app.auth import get_current_user, require_roles
from app.services.freshguard import analyze_image, evaluate_quality_risk, run_safety_engine

router = APIRouter(prefix="/food-batches", tags=["Food Batches"])

UPLOAD_DIR = "uploads/food_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

FOOD_CATEGORIES = [
    "Biryani", "Curry", "Dal", "Cooked Rice", "Roti", "Bread",
    "Cooked Vegetables", "Meat Dishes", "Soup/Stew", "Prepared Meals",
    "Raw Vegetables", "Fruits", "Dairy", "Snacks/Sweets", "Other"
]


class BatchCreate(BaseModel):
    food_category: str
    description: Optional[str] = ""
    quantity_kg: float
    preparation_time: Optional[str] = None
    storage_temp: Optional[str] = "ROOM_TEMP"
    storage_method: Optional[str] = "SEALED"
    packaging_intact: Optional[bool] = True
    handling_completeness: Optional[float] = 0.8
    transport_duration_hours: Optional[float] = 0


class AssessDecision(BaseModel):
    decision: str  # APPROVED or REJECTED
    reason: str


def _batch_dict(b: FoodBatch, include_assessments=False):
    d = {
        "id": b.id,
        "food_category": b.food_category,
        "description": b.description,
        "quantity_kg": b.quantity_kg,
        "status": b.status,
        "storage_temp": b.storage_temp,
        "storage_method": b.storage_method,
        "packaging_intact": b.packaging_intact,
        "handling_completeness": b.handling_completeness,
        "image_path": b.image_path,
        "rejection_reason": b.rejection_reason,
        "preparation_time": b.preparation_time.isoformat() if b.preparation_time else None,
        "created_at": b.created_at.isoformat() if b.created_at else None,
        "updated_at": b.updated_at.isoformat() if b.updated_at else None,
        "donor": {"id": b.donor.id, "name": b.donor.name} if b.donor else None,
    }
    if include_assessments:
        d["model_assessments"] = [
            {"model_name": a.model_name, "output": a.output, "created_at": a.created_at.isoformat()}
            for a in b.model_assessments
        ]
        d["food_assessments"] = [
            {"decision": a.decision, "reason": a.reason, "assessed_at": a.assessed_at.isoformat()}
            for a in b.food_assessments
        ]
    return d


def _log(db, actor, entity_type, entity_id, action, prev=None, new=None):
    db.add(AuditLog(
        actor_id=actor.id if actor else None,
        actor_role=actor.role if actor else None,
        entity_type=entity_type,
        entity_id=entity_id,
        action=action,
        previous_state=prev,
        new_state=new
    ))


@router.get("/categories")
def list_categories():
    return FOOD_CATEGORIES


@router.post("/")
def create_batch(req: BatchCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not current_user.organization_id:
        raise HTTPException(400, "You must belong to an organization to report food")
    if req.quantity_kg <= 0:
        raise HTTPException(400, "Quantity must be greater than 0")

    prep_time = None
    if req.preparation_time:
        try:
            prep_time = datetime.fromisoformat(req.preparation_time.replace("Z", ""))
        except Exception:
            pass

    batch = FoodBatch(
        donor_id=current_user.organization_id,
        food_category=req.food_category,
        description=req.description,
        quantity_kg=req.quantity_kg,
        preparation_time=prep_time,
        storage_temp=req.storage_temp,
        storage_method=req.storage_method,
        packaging_intact=req.packaging_intact,
        handling_completeness=req.handling_completeness,
        transport_duration_hours=req.transport_duration_hours,
        status=BatchStatus.DRAFT,
    )
    db.add(batch)
    db.flush()
    _log(db, current_user, "food_batch", batch.id, "BATCH_CREATED", new={"status": "DRAFT"})
    db.commit()
    db.refresh(batch)
    return _batch_dict(batch)


@router.get("/")
def list_batches(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    q = db.query(FoodBatch)
    if current_user.role == "DONOR":
        q = q.filter(FoodBatch.donor_id == current_user.organization_id)
    elif current_user.role == "RECIPIENT":
        # Show only MATCHING-eligible batches
        q = q.filter(FoodBatch.status == BatchStatus.MATCHING)
    elif current_user.role in ("ASSESSOR", "ADMIN"):
        # Assessors see all batches needing review, including ones with missing info
        q = q.filter(FoodBatch.status.in_([
            BatchStatus.ASSESSMENT_REQUIRED,
            BatchStatus.UNDER_ASSESSMENT,
            BatchStatus.PENDING_INFORMATION,
            BatchStatus.SUBMITTED,
        ]))
    batches = q.order_by(FoodBatch.created_at.desc()).all()
    return [_batch_dict(b) for b in batches]


@router.get("/{batch_id}")
def get_batch(batch_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    batch = db.query(FoodBatch).filter(FoodBatch.id == batch_id).first()
    if not batch:
        raise HTTPException(404, "Batch not found")
    return _batch_dict(batch, include_assessments=True)


@router.post("/{batch_id}/upload-image")
async def upload_image(
    batch_id: str,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    batch = db.query(FoodBatch).filter(FoodBatch.id == batch_id).first()
    if not batch:
        raise HTTPException(404, "Batch not found")

    # Validate file type
    if file.content_type not in ("image/jpeg", "image/png", "image/webp"):
        raise HTTPException(400, "Only JPEG, PNG, and WebP images are accepted")

    # Save file
    ext = file.filename.split(".")[-1] if "." in file.filename else "jpg"
    filename = f"{batch_id}.{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)
    with open(filepath, "wb") as f:
        shutil.copyfileobj(file.file, f)

    batch.image_path = filepath
    db.commit()
    return {"image_path": filepath, "message": "Image uploaded successfully"}


@router.post("/{batch_id}/assess-image")
def assess_image(batch_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    batch = db.query(FoodBatch).filter(FoodBatch.id == batch_id).first()
    if not batch:
        raise HTTPException(404, "Batch not found")

    result = analyze_image(batch.food_category, batch.image_path)

    assessment = ModelAssessment(
        batch_id=batch_id,
        model_name="FreshGuard-Vision",
        prediction_target="visible_quality_classification",
        assessment_method="SIMULATED_VISION",
        input_summary={"food_category": batch.food_category, "has_image": batch.image_path is not None},
        output=result
    )
    db.add(assessment)
    db.commit()
    return result


@router.post("/{batch_id}/assess-risk")
def assess_risk(batch_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    batch = db.query(FoodBatch).filter(FoodBatch.id == batch_id).first()
    if not batch:
        raise HTTPException(404, "Batch not found")

    result = evaluate_quality_risk(
        food_category=batch.food_category,
        preparation_time=batch.preparation_time,
        storage_temp=batch.storage_temp or "ROOM_TEMP",
        storage_method=batch.storage_method,
        packaging_intact=batch.packaging_intact,
        handling_completeness=batch.handling_completeness or 0.5,
        transport_duration_hours=batch.transport_duration_hours or 0,
    )

    assessment = ModelAssessment(
        batch_id=batch_id,
        model_name="FreshGuard-Risk",
        prediction_target="quality_deterioration_risk",
        assessment_method="RULES_BASED",
        input_summary={
            "food_category": batch.food_category,
            "storage_temp": batch.storage_temp,
            "handling_completeness": batch.handling_completeness
        },
        output=result
    )
    db.add(assessment)
    db.commit()
    return result


@router.post("/{batch_id}/submit")
def submit_batch(batch_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    batch = db.query(FoodBatch).filter(FoodBatch.id == batch_id).first()
    if not batch:
        raise HTTPException(404, "Batch not found")
    if batch.status not in (BatchStatus.DRAFT, BatchStatus.PENDING_INFORMATION):
        raise HTTPException(400, f"Cannot submit batch in status: {batch.status}")

    engine_result = run_safety_engine(batch)
    old_status = batch.status
    batch.status = engine_result["recommended_status"]
    batch.updated_at = datetime.utcnow()
    _log(db, current_user, "food_batch", batch_id, "BATCH_SUBMITTED",
         prev={"status": old_status}, new={"status": batch.status})
    db.commit()
    return {"status": batch.status, "flags": engine_result.get("flags", [])}


@router.post("/{batch_id}/approve")
def approve_batch(
    batch_id: str,
    req: AssessDecision,
    current_user: User = Depends(require_roles("ASSESSOR", "ADMIN")),
    db: Session = Depends(get_db)
):
    batch = db.query(FoodBatch).filter(FoodBatch.id == batch_id).first()
    if not batch:
        raise HTTPException(404, "Batch not found")
    if batch.status not in (BatchStatus.ASSESSMENT_REQUIRED, BatchStatus.UNDER_ASSESSMENT, BatchStatus.PENDING_INFORMATION, BatchStatus.SUBMITTED):
        raise HTTPException(400, f"Cannot approve batch in status: {batch.status}")
    if req.decision not in ("APPROVED", "REJECTED"):
        raise HTTPException(400, "Decision must be APPROVED or REJECTED")

    old_status = batch.status
    if req.decision == "APPROVED":
        batch.status = BatchStatus.APPROVED
    else:
        batch.status = BatchStatus.REJECTED
        batch.rejection_reason = req.reason

    batch.updated_at = datetime.utcnow()

    food_assessment = FoodAssessment(
        batch_id=batch_id,
        assessor_id=current_user.id,
        decision=req.decision,
        reason=req.reason,
        findings={"assessor_review": True}
    )
    db.add(food_assessment)
    _log(db, current_user, "food_batch", batch_id, f"BATCH_{req.decision}",
         prev={"status": old_status}, new={"status": batch.status, "reason": req.reason})
    db.commit()

    # If approved, automatically move to MATCHING and generate matches for recipient shelters
    if req.decision == "APPROVED":
        batch.status = BatchStatus.MATCHING
        db.commit()
        try:
            from app.services.freshguard import match_recipients
            from app.models.db_models import RecipientRequirement, DonationMatch, MatchStatus
            reqs = db.query(RecipientRequirement).filter(RecipientRequirement.status == "ACTIVE").all()
            donor = db.query(Organization).filter(Organization.id == batch.donor_id).first()
            scored = match_recipients(batch, reqs, donor.latitude if donor else None, donor.longitude if donor else None)
            for s in scored[:3]:
                if s.get("organization"):
                    m = DonationMatch(
                        batch_id=batch.id,
                        recipient_id=s["organization"].id,
                        offered_quantity_kg=batch.quantity_kg,
                        estimated_distance_km=s.get("estimated_distance_km", 3.5),
                        match_score=s.get("match_score", 92.0),
                        status=MatchStatus.OFFERED
                    )
                    db.add(m)
            batch.status = BatchStatus.MATCHED
            db.commit()
        except Exception as e:
            print("[WARN] Auto-match exception:", e)
    elif req.decision == "REJECTED":
        # Zero-waste diversion: route rejected batch to Gaushala or Compost
        try:
            from app.models.db_models import WasteBatch, WasteStatus
            waste = WasteBatch(
                donor_id=batch.donor_id,
                waste_category="Cooked Food (Diverted)",
                quantity_kg=batch.quantity_kg,
                contamination_status="ORGANIC_CATTLE_FEED",
                contamination_details=f"Diverted safely to Gaushala/Compost: {req.reason}",
                status=WasteStatus.REPORTED
            )
            db.add(waste)
            db.commit()
        except Exception as err:
            print("[WARN] Auto-waste routing exception:", err)

    return {"status": batch.status, "decision": req.decision}


@router.delete("/{batch_id}")
def cancel_batch(batch_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    batch = db.query(FoodBatch).filter(FoodBatch.id == batch_id).first()
    if not batch:
        raise HTTPException(404, "Batch not found")
    batch.status = BatchStatus.CANCELLED
    batch.updated_at = datetime.utcnow()
    db.commit()
    return {"status": "CANCELLED"}
