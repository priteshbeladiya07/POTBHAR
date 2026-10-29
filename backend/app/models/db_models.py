"""
POTBHAR Backend - Database Models (SQLAlchemy)
All tables for the food recovery and organic waste platform.
"""

from datetime import datetime
from sqlalchemy import (
    create_engine, Column, String, Float, Boolean,
    Integer, DateTime, Text, ForeignKey, JSON, Enum as SAEnum
)
from sqlalchemy.orm import DeclarativeBase, relationship, sessionmaker
import uuid
import enum

DATABASE_URL = "sqlite:///./potbhar.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def new_uuid():
    return str(uuid.uuid4())


class Base(DeclarativeBase):
    pass


# ─── Enums ────────────────────────────────────────────────────────────────────

class UserRole(str, enum.Enum):
    DONOR = "DONOR"
    RECIPIENT = "RECIPIENT"
    ASSESSOR = "ASSESSOR"
    PROCESSOR = "PROCESSOR"
    LOGISTICS = "LOGISTICS"
    ADMIN = "ADMIN"


class OrgType(str, enum.Enum):
    DONOR = "DONOR"
    RECIPIENT = "RECIPIENT"
    PROCESSOR = "PROCESSOR"
    LOGISTICS = "LOGISTICS"


class VerificationStatus(str, enum.Enum):
    PENDING = "PENDING"
    VERIFIED = "VERIFIED"
    REJECTED = "REJECTED"
    SUSPENDED = "SUSPENDED"


class BatchStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    SUBMITTED = "SUBMITTED"
    PENDING_INFORMATION = "PENDING_INFORMATION"
    ASSESSMENT_REQUIRED = "ASSESSMENT_REQUIRED"
    UNDER_ASSESSMENT = "UNDER_ASSESSMENT"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    MATCHING = "MATCHING"
    MATCHED = "MATCHED"
    PICKUP_SCHEDULED = "PICKUP_SCHEDULED"
    IN_TRANSIT = "IN_TRANSIT"
    DELIVERED = "DELIVERED"
    EXPIRED = "EXPIRED"
    CANCELLED = "CANCELLED"


class MatchStatus(str, enum.Enum):
    OFFERED = "OFFERED"
    ACCEPTED = "ACCEPTED"
    DECLINED = "DECLINED"
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"


class DeliveryStatus(str, enum.Enum):
    SCHEDULED = "SCHEDULED"
    IN_TRANSIT = "IN_TRANSIT"
    DELIVERED = "DELIVERED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class WasteStatus(str, enum.Enum):
    REPORTED = "REPORTED"
    SCHEDULED = "SCHEDULED"
    COLLECTED = "COLLECTED"
    RECEIVED = "RECEIVED"
    PROCESSED = "PROCESSED"


# ─── Tables ───────────────────────────────────────────────────────────────────

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=new_uuid)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default=UserRole.DONOR)
    organization_id = Column(String, ForeignKey("organizations.id"), nullable=True)
    phone = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    organization = relationship("Organization", back_populates="members", foreign_keys=[organization_id])


class Organization(Base):
    __tablename__ = "organizations"
    id = Column(String, primary_key=True, default=new_uuid)
    name = Column(String, nullable=False)
    organization_type = Column(String, nullable=False)
    address = Column(Text, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    service_area_radius_km = Column(Float, nullable=True, default=25.0)
    verification_status = Column(String, default=VerificationStatus.PENDING)
    contact_information = Column(JSON, default=dict)
    metadata_ = Column("metadata", JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)
    verified_at = Column(DateTime, nullable=True)
    verified_by = Column(String, nullable=True)

    members = relationship("User", back_populates="organization", foreign_keys=[User.organization_id])
    food_batches = relationship("FoodBatch", back_populates="donor", foreign_keys="FoodBatch.donor_id")
    waste_batches = relationship("WasteBatch", back_populates="donor", foreign_keys="WasteBatch.donor_id")


class FoodBatch(Base):
    __tablename__ = "food_batches"
    id = Column(String, primary_key=True, default=new_uuid)
    donor_id = Column(String, ForeignKey("organizations.id"), nullable=False)
    food_category = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    quantity_kg = Column(Float, nullable=False)
    preparation_time = Column(DateTime, nullable=True)
    expiry_estimate = Column(DateTime, nullable=True)
    storage_temp = Column(String, nullable=True, default="ROOM_TEMP")
    storage_method = Column(String, nullable=True)
    packaging_intact = Column(Boolean, nullable=True)
    handling_completeness = Column(Float, default=0.5)
    transport_duration_hours = Column(Float, nullable=True, default=0)
    image_path = Column(String, nullable=True)
    status = Column(String, default=BatchStatus.DRAFT)
    rejection_reason = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    donor = relationship("Organization", back_populates="food_batches")
    model_assessments = relationship("ModelAssessment", back_populates="batch")
    food_assessments = relationship("FoodAssessment", back_populates="batch")
    matches = relationship("DonationMatch", back_populates="batch")


class ModelAssessment(Base):
    __tablename__ = "model_assessments"
    id = Column(String, primary_key=True, default=new_uuid)
    batch_id = Column(String, ForeignKey("food_batches.id"), nullable=False)
    model_name = Column(String, nullable=False)
    model_version = Column(String, default="1.0.0")
    assessment_method = Column(String, default="RULES_BASED")
    prediction_target = Column(String, nullable=False)
    input_summary = Column(JSON, default=dict)
    output = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)

    batch = relationship("FoodBatch", back_populates="model_assessments")


class FoodAssessment(Base):
    __tablename__ = "food_assessments"
    id = Column(String, primary_key=True, default=new_uuid)
    batch_id = Column(String, ForeignKey("food_batches.id"), nullable=False)
    assessor_id = Column(String, ForeignKey("users.id"), nullable=False)
    decision = Column(String, nullable=False)
    findings = Column(JSON, default=dict)
    rule_version = Column(String, default="1.0")
    reason = Column(Text, nullable=False)
    assessed_at = Column(DateTime, default=datetime.utcnow)

    batch = relationship("FoodBatch", back_populates="food_assessments")
    assessor = relationship("User")


class RecipientRequirement(Base):
    __tablename__ = "recipient_requirements"
    id = Column(String, primary_key=True, default=new_uuid)
    recipient_id = Column(String, ForeignKey("organizations.id"), nullable=False)
    food_category = Column(String, nullable=False)
    quantity_needed_kg = Column(Float, nullable=False)
    capacity_kg = Column(Float, nullable=False)
    available_from = Column(DateTime, nullable=True)
    available_until = Column(DateTime, nullable=True)
    dietary_constraints = Column(JSON, default=list)
    status = Column(String, default="ACTIVE")
    created_at = Column(DateTime, default=datetime.utcnow)

    recipient = relationship("Organization")


class DonationMatch(Base):
    __tablename__ = "donation_matches"
    id = Column(String, primary_key=True, default=new_uuid)
    batch_id = Column(String, ForeignKey("food_batches.id"), nullable=False)
    recipient_id = Column(String, ForeignKey("organizations.id"), nullable=False)
    offered_quantity_kg = Column(Float, nullable=False)
    accepted_quantity_kg = Column(Float, nullable=True)
    estimated_distance_km = Column(Float, nullable=True)
    match_score = Column(Float, nullable=True)
    status = Column(String, default=MatchStatus.OFFERED)
    created_at = Column(DateTime, default=datetime.utcnow)
    responded_at = Column(DateTime, nullable=True)

    batch = relationship("FoodBatch", back_populates="matches")
    recipient = relationship("Organization")
    delivery = relationship("Delivery", back_populates="match", uselist=False)


class Delivery(Base):
    __tablename__ = "deliveries"
    id = Column(String, primary_key=True, default=new_uuid)
    match_id = Column(String, ForeignKey("donation_matches.id"), nullable=False)
    scheduled_pickup = Column(DateTime, nullable=True)
    actual_pickup = Column(DateTime, nullable=True)
    actual_delivery = Column(DateTime, nullable=True)
    dispatched_quantity_kg = Column(Float, nullable=True)
    delivered_quantity_kg = Column(Float, nullable=True)
    status = Column(String, default=DeliveryStatus.SCHEDULED)
    recipient_confirmation = Column(JSON, nullable=True)
    exception_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    match = relationship("DonationMatch", back_populates="delivery")


class WasteBatch(Base):
    __tablename__ = "waste_batches"
    id = Column(String, primary_key=True, default=new_uuid)
    donor_id = Column(String, ForeignKey("organizations.id"), nullable=False)
    waste_category = Column(String, nullable=False)
    quantity_kg = Column(Float, nullable=False)
    contamination_status = Column(String, default="UNKNOWN")
    contamination_details = Column(Text, nullable=True)
    processor_id = Column(String, ForeignKey("organizations.id"), nullable=True)
    status = Column(String, default=WasteStatus.REPORTED)
    received_quantity_kg = Column(Float, nullable=True)
    processing_outcome = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    donor = relationship("Organization", back_populates="waste_batches", foreign_keys=[donor_id])
    processor = relationship("Organization", foreign_keys=[processor_id])


class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(String, primary_key=True, default=new_uuid)
    actor_id = Column(String, nullable=True)
    actor_role = Column(String, nullable=True)
    entity_type = Column(String, nullable=False)
    entity_id = Column(String, nullable=False)
    action = Column(String, nullable=False)
    previous_state = Column(JSON, nullable=True)
    new_state = Column(JSON, nullable=True)
    metadata_ = Column("metadata", JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)


def create_tables():
    Base.metadata.create_all(bind=engine)
