"""
seed_demo_data.py - Seed realistic demo batches across all pipeline stages:
1. ASSESSMENT_REQUIRED (ready for Assessor to approve or reject)
2. MATCHED / OFFERED (ready for Recipient to accept)
3. SCHEDULED Delivery (ready for Rider to pick up and deliver)
4. DELIVERED Delivery (historical impact data for analytics)
5. Organic Waste Batch (for Gaushala/Compost processor)
"""

from datetime import datetime, timedelta
from app.models.db_models import (
    SessionLocal, FoodBatch, DonationMatch, Delivery, WasteBatch,
    BatchStatus, MatchStatus, DeliveryStatus, WasteStatus,
    Organization, RecipientRequirement
)
import uuid

def seed():
    db = SessionLocal()
    try:
        donor_org = db.query(Organization).filter(Organization.organization_type == "DONOR").first()
        recipient_org = db.query(Organization).filter(Organization.organization_type == "RECIPIENT").first()
        processor_org = db.query(Organization).filter(Organization.organization_type == "PROCESSOR").first()

        if not donor_org or not recipient_org:
            print("Required organizations missing, skipping.")
            return

        now = datetime.utcnow()

        # Ensure Recipient Requirements exist
        categories = ["Curry", "Biryani", "Cooked Rice", "Dal", "Cooked Vegetables"]
        for cat in categories:
            existing = db.query(RecipientRequirement).filter(
                RecipientRequirement.recipient_id == recipient_org.id,
                RecipientRequirement.food_category == cat
            ).first()
            if not existing:
                req = RecipientRequirement(
                    id=str(uuid.uuid4()),
                    recipient_id=recipient_org.id,
                    food_category=cat,
                    quantity_needed_kg=30.0,
                    capacity_kg=60.0,
                    status="ACTIVE",
                    created_at=now - timedelta(hours=2)
                )
                db.add(req)

        # 1. Batch in ASSESSMENT_REQUIRED (for Checker/Assessor)
        batch_assess = FoodBatch(
            id=str(uuid.uuid4()),
            donor_id=donor_org.id,
            food_category="Curry",
            description="Shahi Paneer and Butter Roti from corporate catering banquet. Kept hot in food warmers.",
            quantity_kg=42.0,
            preparation_time=now - timedelta(hours=1, minutes=30),
            storage_temp="ROOM_TEMP",
            storage_method="INSULATED_BOX",
            packaging_intact=True,
            handling_completeness=0.92,
            status=BatchStatus.ASSESSMENT_REQUIRED,
            created_at=now - timedelta(minutes=45)
        )
        db.add(batch_assess)

        # 2. Batch in MATCHED / OFFERED (for Recipient to accept)
        batch_offer = FoodBatch(
            id=str(uuid.uuid4()),
            donor_id=donor_org.id,
            food_category="Biryani",
            description="Vegetable Dum Biryani prepared for festival event. Chilled and packed in food-grade containers.",
            quantity_kg=35.0,
            preparation_time=now - timedelta(hours=2),
            storage_temp="CHILLED",
            storage_method="SEALED",
            packaging_intact=True,
            handling_completeness=0.88,
            status=BatchStatus.MATCHED,
            created_at=now - timedelta(hours=1, minutes=15)
        )
        db.add(batch_offer)

        match_offer = DonationMatch(
            id=str(uuid.uuid4()),
            batch_id=batch_offer.id,
            recipient_id=recipient_org.id,
            offered_quantity_kg=35.0,
            estimated_distance_km=4.2,
            match_score=0.94,
            status=MatchStatus.OFFERED,
            created_at=now - timedelta(minutes=30)
        )
        db.add(match_offer)

        # 3. Batch with SCHEDULED Delivery (for Rider to pick up)
        batch_delivery = FoodBatch(
            id=str(uuid.uuid4()),
            donor_id=donor_org.id,
            food_category="Dal",
            description="Tadka Dal and Jeera Rice, freshly cooked and sealed in stainless steel dispatch urns.",
            quantity_kg=28.0,
            preparation_time=now - timedelta(hours=2, minutes=30),
            storage_temp="ROOM_TEMP",
            storage_method="SEALED",
            packaging_intact=True,
            handling_completeness=0.90,
            status=BatchStatus.PICKUP_SCHEDULED,
            created_at=now - timedelta(hours=2)
        )
        db.add(batch_delivery)

        match_delivery = DonationMatch(
            id=str(uuid.uuid4()),
            batch_id=batch_delivery.id,
            recipient_id=recipient_org.id,
            offered_quantity_kg=28.0,
            accepted_quantity_kg=28.0,
            estimated_distance_km=5.8,
            match_score=0.91,
            status=MatchStatus.ACCEPTED,
            created_at=now - timedelta(hours=1),
            responded_at=now - timedelta(minutes=50)
        )
        db.add(match_delivery)

        delivery_active = Delivery(
            id=str(uuid.uuid4()),
            match_id=match_delivery.id,
            scheduled_pickup=now + timedelta(minutes=15),
            dispatched_quantity_kg=28.0,
            status=DeliveryStatus.SCHEDULED
        )
        db.add(delivery_active)

        # 4. Historical DELIVERED Batch (for rich Analytics)
        batch_past = FoodBatch(
            id=str(uuid.uuid4()),
            donor_id=donor_org.id,
            food_category="Cooked Rice",
            description="Steamed Basmati Rice & Mixed Dal from community kitchen dinner.",
            quantity_kg=65.0,
            preparation_time=now - timedelta(days=1, hours=4),
            storage_temp="ROOM_TEMP",
            storage_method="SEALED",
            packaging_intact=True,
            handling_completeness=0.95,
            status=BatchStatus.DELIVERED,
            created_at=now - timedelta(days=1)
        )
        db.add(batch_past)

        match_past = DonationMatch(
            id=str(uuid.uuid4()),
            batch_id=batch_past.id,
            recipient_id=recipient_org.id,
            offered_quantity_kg=65.0,
            accepted_quantity_kg=65.0,
            estimated_distance_km=3.5,
            match_score=0.96,
            status=MatchStatus.COMPLETED,
            created_at=now - timedelta(days=1),
            responded_at=now - timedelta(days=1)
        )
        db.add(match_past)

        delivery_past = Delivery(
            id=str(uuid.uuid4()),
            match_id=match_past.id,
            scheduled_pickup=now - timedelta(days=1, hours=2),
            actual_pickup=now - timedelta(days=1, hours=1, minutes=45),
            actual_delivery=now - timedelta(days=1, hours=1),
            dispatched_quantity_kg=65.0,
            delivered_quantity_kg=65.0,
            status=DeliveryStatus.DELIVERED,
            recipient_confirmation={"signature": "Verified", "temp_ok": True}
        )
        db.add(delivery_past)

        # 5. Waste Batch for Gaushala/Compost
        if processor_org:
            waste = WasteBatch(
                id=str(uuid.uuid4()),
                donor_id=donor_org.id,
                waste_category="ORGANIC_CATTLE_FEED",
                quantity_kg=55.0,
                status=WasteStatus.SCHEDULED,
                processor_id=processor_org.id,
                created_at=now - timedelta(hours=4)
            )
            db.add(waste)

        db.commit()
        print("Successfully seeded realistic demo batches across all 4 roles!")
    except Exception as e:
        db.rollback()
        print(f"Error seeding data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
