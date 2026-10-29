"""Auth router — register, login, me"""
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from app.models.db_models import get_db, User, Organization, AuditLog
from app.auth import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])


class RegisterRequest(BaseModel):
    full_name: str
    email: str
    password: str
    role: str = "DONOR"
    phone: str = ""


class OrgCreate(BaseModel):
    name: str
    organization_type: str
    address: str = ""
    latitude: float = None
    longitude: float = None


@router.post("/register")
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == req.email).first():
        raise HTTPException(400, "Email already registered")
    allowed_roles = ["DONOR", "RECIPIENT", "ASSESSOR", "PROCESSOR", "LOGISTICS", "ADMIN"]
    if req.role not in allowed_roles:
        raise HTTPException(400, f"Invalid role. Choose from: {allowed_roles}")
    user = User(
        full_name=req.full_name,
        email=req.email,
        hashed_password=hash_password(req.password),
        role=req.role,
        phone=req.phone,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_access_token({"sub": user.id, "role": user.role})
    return {"access_token": token, "token_type": "bearer", "user": _user_dict(user)}


@router.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form.username).first()
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(401, "Invalid credentials")
    token = create_access_token({"sub": user.id, "role": user.role})
    return {"access_token": token, "token_type": "bearer", "user": _user_dict(user)}


@router.get("/me")
def me(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    org = None
    if current_user.organization_id:
        org = db.query(Organization).filter(Organization.id == current_user.organization_id).first()
    return {**_user_dict(current_user), "organization": _org_dict(org) if org else None}


@router.post("/create-organization")
def create_org(org: OrgCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    new_org = Organization(
        name=org.name,
        organization_type=org.organization_type,
        address=org.address,
        latitude=org.latitude,
        longitude=org.longitude,
    )
    db.add(new_org)
    db.flush()
    current_user.organization_id = new_org.id
    db.commit()
    db.refresh(new_org)
    return _org_dict(new_org)


def _user_dict(u: User):
    return {
        "id": u.id, "full_name": u.full_name, "email": u.email,
        "role": u.role, "phone": u.phone,
        "organization_id": u.organization_id,
        "created_at": u.created_at.isoformat() if u.created_at else None
    }

def _org_dict(o: Organization):
    if not o: return None
    return {
        "id": o.id, "name": o.name, "organization_type": o.organization_type,
        "address": o.address, "latitude": o.latitude, "longitude": o.longitude,
        "verification_status": o.verification_status,
        "created_at": o.created_at.isoformat() if o.created_at else None
    }
