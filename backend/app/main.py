"""
POTBHAR FastAPI Main Application
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.models.db_models import create_tables
from app.routers.auth import router as auth_router
from app.routers.food_batches import router as batches_router
from app.routers.all_routers import (
    orgs_router, reqs_router, match_router,
    delivery_router, waste_router, analytics_router
)
from app.routers.smart_donation import router as smart_donation_router

app = FastAPI(
    title="POTBHAR API",
    description="AI-Powered Food Recovery, Quality Assessment & Organic Waste Management",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174", "http://localhost:5173", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all routers
PREFIX = "/api/v1"
app.include_router(auth_router, prefix=PREFIX)
app.include_router(batches_router, prefix=PREFIX)
app.include_router(orgs_router, prefix=PREFIX)
app.include_router(reqs_router, prefix=PREFIX)
app.include_router(match_router, prefix=PREFIX)
app.include_router(delivery_router, prefix=PREFIX)
app.include_router(waste_router, prefix=PREFIX)
app.include_router(analytics_router, prefix=PREFIX)
app.include_router(smart_donation_router, prefix=PREFIX)

# Serve uploaded images
os.makedirs("uploads/food_images", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


@app.on_event("startup")
def startup():
    create_tables()
    _seed_demo_data()
    print("[OK] POTBHAR API started. Visit http://localhost:8000/docs")


@app.get("/")
def root():
    return {
        "name": "POTBHAR API",
        "tagline": "Har Pet Bhare, Har Nivala Sambhale",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running"
    }


@app.get("/api/v1/health")
def health():
    return {"status": "healthy", "service": "POTBHAR"}


def _seed_demo_data():
    """Seed demo data on first run."""
    from app.models.db_models import SessionLocal, User, Organization
    from app.auth import hash_password
    db = SessionLocal()
    try:
        if db.query(User).count() > 0:
            return  # Already seeded

        # Create demo organizations
        orgs = [
            Organization(name="Green Feast Caterers", organization_type="DONOR", address="Connaught Place, New Delhi",
                         latitude=28.6315, longitude=77.2167, verification_status="VERIFIED"),
            Organization(name="Asha NGO - Food Bank", organization_type="RECIPIENT", address="Lajpat Nagar, New Delhi",
                         latitude=28.5700, longitude=77.2400, verification_status="VERIFIED", service_area_radius_km=20),
            Organization(name="EcoCompost Delhi", organization_type="PROCESSOR", address="Okhla Industrial Area, New Delhi",
                         latitude=28.5350, longitude=77.2710, verification_status="VERIFIED", service_area_radius_km=30),
            Organization(name="Nourish Foundation", organization_type="RECIPIENT", address="Karol Bagh, New Delhi",
                         latitude=28.6517, longitude=77.1887, verification_status="VERIFIED", service_area_radius_km=15),
        ]
        for o in orgs:
            db.add(o)
        db.flush()

        # Create demo users
        users = [
            User(full_name="Ravi Sharma", email="donor@potbhar.demo", hashed_password=hash_password("demo123"),
                 role="DONOR", organization_id=orgs[0].id),
            User(full_name="Priya Nair", email="recipient@potbhar.demo", hashed_password=hash_password("demo123"),
                 role="RECIPIENT", organization_id=orgs[1].id),
            User(full_name="Dr. Ananya Verma", email="assessor@potbhar.demo", hashed_password=hash_password("demo123"),
                 role="ASSESSOR", organization_id=orgs[0].id),
            User(full_name="Suresh Kumar", email="admin@potbhar.demo", hashed_password=hash_password("demo123"),
                 role="ADMIN"),
            User(full_name="EcoProcessor", email="processor@potbhar.demo", hashed_password=hash_password("demo123"),
                 role="PROCESSOR", organization_id=orgs[2].id),
        ]
        for u in users:
            db.add(u)
        db.flush()

        # Create recipient requirements
        from app.models.db_models import RecipientRequirement
        reqs = [
            RecipientRequirement(recipient_id=orgs[1].id, food_category="Biryani",
                                  quantity_needed_kg=30, capacity_kg=50, status="ACTIVE"),
            RecipientRequirement(recipient_id=orgs[1].id, food_category="Dal",
                                  quantity_needed_kg=15, capacity_kg=25, status="ACTIVE"),
            RecipientRequirement(recipient_id=orgs[3].id, food_category="Cooked Rice",
                                  quantity_needed_kg=20, capacity_kg=40, status="ACTIVE"),
        ]
        for r in reqs:
            db.add(r)

        db.commit()
        print("[OK] Demo data seeded. Login: donor@potbhar.demo / demo123")
        print("     Also: assessor@potbhar.demo, recipient@potbhar.demo, admin@potbhar.demo (all: demo123)")

    except Exception as e:
        print(f"[WARN] Seed error (may already be seeded): {e}")
        db.rollback()
    finally:
        db.close()
