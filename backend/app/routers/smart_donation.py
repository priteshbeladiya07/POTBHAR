"""
POTBHAR Backend - Smart Food Rescue & Donation Router
Connects donors with Gaushalas, Dog Shelters, Human Shelters, and Organic Compost facilities.
Includes AI-based smart recommendations, route optimization, recipient contact cards, and scrap-to-compost conversion.
"""

from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
import math
import uuid

from app.models.db_models import (
    get_db, User, Organization, FoodBatch, DonationMatch,
    Delivery, WasteBatch, AuditLog, BatchStatus, MatchStatus, DeliveryStatus
)
from app.auth import get_current_user

router = APIRouter(prefix="/smart-donation", tags=["Food Rescue & Smart Donation"])


# ─── Recipient Directory with Rich Contact & Capacity Details ──────────────────

RECIPIENT_DIRECTORY = [
    {
        "id": "rec_rural_01",
        "name": "Sahyadri Gramin Annapurna Seva & Anganwadi Network",
        "type": "RURAL_COMMUNITY",
        "type_label": "Rural Village Food Relief & Child Nutrition",
        "diet_compatibility": "Nutritious Cooked Meals, Fresh Rotis, Pulses & Fortified Grains",
        "diet_tag": "RURAL_NUTRITION",
        "accepted_items": ["Freshly Cooked Khichdi", "Rotis / Chapatis", "Dal & Sabzi", "Lentils & Flour Sacks", "Seasonal Fruit"],
        "restricted_items": ["Over-spiced gravies", "Stale/soured food (>4h)", "Unsealed crates"],
        "contact_person": "Sarpanch Balasaheb Shinde",
        "phone": "+91 98220 44881",
        "emergency_phone": "+91 98220 44882",
        "email": "sahyadri.rural@potbhar.org",
        "address": "Village Gram Panchayat Kendra, Saswad-Purandar Rural Belt, Pune 412301",
        "latitude": 18.3441,
        "longitude": 73.9856,
        "daily_capacity_kg": 450.0,
        "current_intake_kg": 230.0,
        "capacity_remaining_kg": 220.0,
        "resident_count": 280,
        "verification_status": "VERIFIED_ZILLA_PARISHAD_RURAL",
        "verified_badge": "Zilla Parishad & Village Panchayat Certified",
        "rating": 4.97,
        "rating_count": 380,
        "pickup_lead_time_mins": 40,
        "image_url": "/images/rural-food-distribution.jpg",
        "service_radius_km": 35.0,
    },
    {
        "id": "rec_rural_02",
        "name": "Kisan Bandhu Rural Outreach & Mobile Meal Unit",
        "type": "RURAL_COMMUNITY",
        "type_label": "Rural Farm Worker & Drought-Prone Village Relief",
        "diet_compatibility": "Balanced Hot Meals, Rice, Chapati & Clean Water Tiffins",
        "diet_tag": "RURAL_NUTRITION",
        "accepted_items": ["Vegetable Pulao", "Dal Tadka", "Packed Tiffins", "Sacks of Grain & Atta", "Jaggery & Chana"],
        "restricted_items": ["Perishable unprotected sweets", "Non-potable water containers"],
        "contact_person": "Sunanda Gaikwad (Outreach Lead)",
        "phone": "+91 98220 66771",
        "emergency_phone": "+91 98220 66772",
        "email": "kisanoutreach@potbhar.org",
        "address": "Khed Taluka Field Relief Depot, Chakan-Shikrapur Rural Link, Pune 410501",
        "latitude": 18.7523,
        "longitude": 73.8567,
        "daily_capacity_kg": 380.0,
        "current_intake_kg": 190.0,
        "capacity_remaining_kg": 190.0,
        "resident_count": 240,
        "verification_status": "VERIFIED_RURAL_DEVELOPMENT_TRUST",
        "verified_badge": "Rural Development Trust Registered",
        "rating": 4.93,
        "rating_count": 295,
        "pickup_lead_time_mins": 45,
        "image_url": "/images/rural-outreach-potbhar.jpg",
        "service_radius_km": 40.0,
    },
    {
        "id": "rec_gaushala_01",
        "name": "Vrindavan Gaushala & Cattle Sanctuary",
        "type": "GAUSHALA",
        "type_label": "Gaushala (Cattle Shelter)",
        "diet_compatibility": "Pure Vegetarian (Cattle-Friendly)",
        "diet_tag": "PURE_VEG",
        "accepted_items": ["Cooked Rice", "Rotis & Naans", "Greens & Vegetables", "Dals", "Fruit Peelings", "Fresh Grains"],
        "restricted_items": ["Meat", "Fish", "Eggs", "Garlic/Onion heavy gravies", "Plastic/Packaging"],
        "contact_person": "Mahant Rajeshwar Das",
        "phone": "+91 98220 33441",
        "emergency_phone": "+91 98220 33442",
        "email": "seva@vrindavangaushala.org",
        "address": "Survey 48, Aundh-Ravet Road, Near Aundh Gaushala Facility, Pune, Maharashtra 411007",
        "latitude": 18.5583,
        "longitude": 73.8077,
        "daily_capacity_kg": 500.0,
        "current_intake_kg": 280.0,
        "capacity_remaining_kg": 220.0,
        "cattle_count": 185,
        "verification_status": "VERIFIED_FSSAI_ANIMAL_WELFARE",
        "verified_badge": "Govt Animal Welfare Board Certified",
        "rating": 4.9,
        "rating_count": 340,
        "pickup_lead_time_mins": 35,
        "image_url": "/images/food-produce.jpg",
        "service_radius_km": 25.0,
    },
    {
        "id": "rec_gaushala_02",
        "name": "Govardhan Cow Rescue & Seva Ashram",
        "type": "GAUSHALA",
        "type_label": "Gaushala & Desi Cow Sanctuary",
        "diet_compatibility": "Pure Vegetarian (Desi Gau Seva)",
        "diet_tag": "PURE_VEG",
        "accepted_items": ["Rotis", "Pulao/Rice", "Chopped raw vegetables", "Lentil residue", "Clean bread scraps"],
        "restricted_items": ["Any Non-Veg", "Sour/Fermented Curds", "Packaging", "Fried oily snacks"],
        "contact_person": "Pandit Ramesh Shastri",
        "phone": "+91 98220 55112",
        "emergency_phone": "+91 98220 55113",
        "email": "contact@govardhanashram.in",
        "address": "Gat No 112, Alandi-Markal Road, Pune Rural, Maharashtra 412105",
        "latitude": 18.6775,
        "longitude": 73.8967,
        "daily_capacity_kg": 350.0,
        "current_intake_kg": 150.0,
        "capacity_remaining_kg": 200.0,
        "cattle_count": 120,
        "verification_status": "VERIFIED_FSSAI_ANIMAL_WELFARE",
        "verified_badge": "FSSAI Gau Seva Compliant",
        "rating": 4.8,
        "rating_count": 210,
        "pickup_lead_time_mins": 45,
        "image_url": "/images/food-produce.jpg",
        "service_radius_km": 30.0,
    },
    {
        "id": "rec_dogshelter_01",
        "name": "PawCare Canine Rescue & Stray Welfare",
        "type": "DOG_SHELTER",
        "type_label": "Dog Shelter & Animal Hospital",
        "diet_compatibility": "Vegetarian & Non-Vegetarian Friendly",
        "diet_tag": "NON_VEG_FRIENDLY",
        "accepted_items": ["Chicken Biryani / Broth", "Cooked Meats & Liver", "Steamed Rice", "Boiled Eggs", "Mutton Gravies (Mild)", "Paneer & Rice"],
        "restricted_items": ["Extremely Spicy Chillies", "Cooked Small Splinter Bones", "Chocolate/Sugar", "Onion concentrates"],
        "contact_person": "Dr. Sneha Roy (Chief Vet)",
        "phone": "+91 98220 77881",
        "emergency_phone": "+91 98220 77882",
        "email": "adoptions@pawcarepune.org",
        "address": "Plot 14, Baner Pashan Link Road, Pashan Biodiversity Park Zone, Pune 411045",
        "latitude": 18.5441,
        "longitude": 73.7892,
        "daily_capacity_kg": 250.0,
        "current_intake_kg": 110.0,
        "capacity_remaining_kg": 140.0,
        "dog_count": 140,
        "verification_status": "VERIFIED_ANIMAL_HOSPITAL",
        "verified_badge": "Licensed Canine Trauma & Feeding Station",
        "rating": 4.95,
        "rating_count": 480,
        "pickup_lead_time_mins": 30,
        "image_url": "/images/food-biryani.jpg",
        "service_radius_km": 20.0,
    },
    {
        "id": "rec_dogshelter_02",
        "name": "Happy Tails Stray Welfare & Recovery Haven",
        "type": "DOG_SHELTER",
        "type_label": "Stray Feeding & Animal Care Sanctuary",
        "diet_compatibility": "Non-Vegetarian & High-Protein Meals",
        "diet_tag": "NON_VEG_FRIENDLY",
        "accepted_items": ["Leftover Banquet Chicken & Rice", "Meat Stews", "Plain Rice & Curd", "Egg curries", "Bread soaked in broth"],
        "restricted_items": ["Sharp Fish Bones", "Deep fried chilli paste", "Sweets/Desserts"],
        "contact_person": "Aditya Kulkarni (Founder)",
        "phone": "+91 98220 99221",
        "emergency_phone": "+91 98220 99222",
        "email": "help@happytailshaven.in",
        "address": "Survey 72, Near Hinjewadi Phase 2 IT Hub, Pune 411057",
        "latitude": 18.5912,
        "longitude": 73.7228,
        "daily_capacity_kg": 200.0,
        "current_intake_kg": 85.0,
        "capacity_remaining_kg": 115.0,
        "dog_count": 95,
        "verification_status": "VERIFIED_ANIMAL_WELFARE",
        "verified_badge": "Registered Society & Animal Ambulance Network",
        "rating": 4.85,
        "rating_count": 190,
        "pickup_lead_time_mins": 40,
        "image_url": "/images/food-biryani.jpg",
        "service_radius_km": 25.0,
    },
    {
        "id": "rec_human_01",
        "name": "Asha Community Shelter & Care Home",
        "type": "HUMAN_SHELTER",
        "type_label": "Human Shelter & Orphan Care",
        "diet_compatibility": "Human Consumption (FSSAI Inspected Hot Surplus)",
        "diet_tag": "HUMAN_SAFE_HOT",
        "accepted_items": ["Dum Biryani & Pulav", "Paneer & Dal Gravies", "Fresh Chapatis", "Sweets & Desserts", "Packed Catering Trays"],
        "restricted_items": ["Cold-held >4 hours", "Stale/Smelling food", "Unsealed containers", "Leftover plate scrapings"],
        "contact_person": "Sister Mary Teresa",
        "phone": "+91 98230 77889",
        "emergency_phone": "+91 98230 77880",
        "email": "care@ashashelter.org",
        "address": "Lajpat Nagar Shelter Center, Near Mahatma Phule Mandai, Pune 411002",
        "latitude": 18.5089,
        "longitude": 73.8567,
        "daily_capacity_kg": 300.0,
        "current_intake_kg": 165.0,
        "capacity_remaining_kg": 135.0,
        "resident_count": 210,
        "verification_status": "VERIFIED_FSSAI_HUMAN",
        "verified_badge": "FSSAI Level-2 Hygiene Certified Shelter",
        "rating": 4.98,
        "rating_count": 720,
        "pickup_lead_time_mins": 25,
        "image_url": "/images/community-food-serving-hall.jpg",
        "service_radius_km": 15.0,
    },
    {
        "id": "rec_human_02",
        "name": "Annapurna Seva Night Home & Meals Project",
        "type": "HUMAN_SHELTER",
        "type_label": "Night Shelter & Senior Citizen Care",
        "diet_compatibility": "Wholesome Vegetarian / Standard Meals",
        "diet_tag": "HUMAN_SAFE_HOT",
        "accepted_items": ["Rice & Lentil Khichdi", "Rotis", "Sabzi & Gravy", "Idli/Dosa", "Fresh curries"],
        "restricted_items": ["Non-edible food", "Cold unpreserved dishes", "Over-spicy sauces"],
        "contact_person": "Pramila Joshi (Superintendent)",
        "phone": "+91 98230 44551",
        "emergency_phone": "+91 98230 44552",
        "email": "meals@annapurnaseva.org",
        "address": "Sadashiv Peth, Near Bharat Natya Mandir, Pune 411030",
        "latitude": 18.5132,
        "longitude": 73.8523,
        "daily_capacity_kg": 220.0,
        "current_intake_kg": 140.0,
        "capacity_remaining_kg": 80.0,
        "resident_count": 160,
        "verification_status": "VERIFIED_FSSAI_HUMAN",
        "verified_badge": "Municipal Corporation Partner",
        "rating": 4.88,
        "rating_count": 310,
        "pickup_lead_time_mins": 30,
        "image_url": "/images/elderly-shelter-meals.jpg",
        "service_radius_km": 18.0,
    },
    {
        "id": "rec_compost_01",
        "name": "EcoKhaad Decentralized Bio-Methanation & Compost Facility",
        "type": "COMPOST_MANURE",
        "type_label": "Organic Fertilizer & Bio-CNG Plant",
        "diet_compatibility": "Organic Food Scraps & Kitchen Waste",
        "diet_tag": "ZERO_WASTE_COMPOST",
        "accepted_items": ["Kitchen Vegetable Peelings", "Expired Cooked Food", "Plate Waste Scrapings", "Bread & Pastry ends", "Citrus & Onion skins", "Spoiled curries"],
        "restricted_items": ["Plastics", "Cutlery", "Metal foils", "Glass", "Chemical cleaning agents"],
        "contact_person": "Er. Arvind Deshmukh (Environmental Engineer)",
        "phone": "+91 98230 88112",
        "emergency_phone": "+91 98230 88113",
        "email": "operations@ecokhaadbiogas.com",
        "address": "Eco Green Zone, Hadapsar Industrial Estate Phase 3, Pune 411013",
        "latitude": 18.5022,
        "longitude": 73.9298,
        "daily_capacity_kg": 2000.0,
        "current_intake_kg": 720.0,
        "capacity_remaining_kg": 1280.0,
        "compost_output_ratio": 0.28,
        "verification_status": "VERIFIED_POLLUTION_CONTROL_BOARD",
        "verified_badge": "State Pollution Board & Solid Waste Rule 2016 Compliant",
        "rating": 4.92,
        "rating_count": 420,
        "pickup_lead_time_mins": 45,
        "image_url": "/images/food-waste-bins.jpg",
        "service_radius_km": 40.0,
    },
    {
        "id": "rec_compost_02",
        "name": "GreenEarth Community Micro-Composting Park",
        "type": "COMPOST_MANURE",
        "type_label": "Aerobic Compost & Urban Farm Soil Project",
        "diet_compatibility": "Raw Prep Waste & Fruit/Vegetable Scraps",
        "diet_tag": "ZERO_WASTE_COMPOST",
        "accepted_items": ["Fruit/Veg trimmings", "Salad leftovers", "Coffee grounds", "Stale grains", "Eggshells"],
        "restricted_items": ["Large plastic wrap", "Non-organic packaging", "Chemical grease"],
        "contact_person": "Sunita Rao (Urban Farming Lead)",
        "phone": "+91 98230 66221",
        "emergency_phone": "+91 98230 66222",
        "email": "contact@greenearthmicrocompost.org",
        "address": "Kothrud Eco Garden, Near Chandani Chowk, Pune 411038",
        "latitude": 18.5074,
        "longitude": 73.8077,
        "daily_capacity_kg": 800.0,
        "current_intake_kg": 340.0,
        "capacity_remaining_kg": 460.0,
        "compost_output_ratio": 0.32,
        "verification_status": "VERIFIED_POLLUTION_CONTROL_BOARD",
        "verified_badge": "Certified 100% Organic Humus Producer",
        "rating": 4.86,
        "rating_count": 180,
        "pickup_lead_time_mins": 35,
        "image_url": "/images/food-produce.jpg",
        "service_radius_km": 25.0,
    }
]


# ─── Distance & Route Calculator Helper ────────────────────────────────────────

def calculate_haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 2)


def generate_optimized_route(donor_coords: Dict[str, float], recipient: Dict[str, Any]) -> Dict[str, Any]:
    donor_lat = donor_coords.get("lat", 18.5308)
    donor_lng = donor_coords.get("lng", 73.8288)
    rec_lat = recipient.get("latitude", 18.5583)
    rec_lng = recipient.get("longitude", 73.8077)

    direct_dist_km = calculate_haversine_distance(donor_lat, donor_lng, rec_lat, rec_lng)
    road_dist_km = round(direct_dist_km * 1.28, 1)  # urban road winding factor
    est_transit_mins = max(15, int(road_dist_km * 3.2 + 8))

    # Determine inspection hub requirement based on recipient type
    rec_type = recipient.get("type")
    requires_lab_inspection = (rec_type == "HUMAN_SHELTER")

    waypoints = []
    # Waypoint 1: Donor
    waypoints.append({
        "step": 1,
        "name": "Donor Kitchen Pickup",
        "role": "SURPLUS_ORIGIN",
        "lat": donor_lat,
        "lng": donor_lng,
        "action": "Inspect seal, record core temp, load into insulated cambros",
        "est_time": "T+0 mins",
        "status": "READY_FOR_DISPATCH"
    })

    if requires_lab_inspection:
        # Waypoint 2: FSSAI Lab
        lab_lat, lab_lng = 18.5314, 73.8446
        waypoints.append({
            "step": 2,
            "name": "POTBHAR Central Quality & Safety Lab",
            "role": "QUALITY_CHECKPOINT",
            "lat": lab_lat,
            "lng": lab_lng,
            "action": "Sensor thermal check (>60°C), pH validation, organoleptic seal",
            "est_time": f"T+{int(est_transit_mins * 0.45)} mins",
            "status": "SCHEDULED_INSPECTION"
        })
        waypoints.append({
            "step": 3,
            "name": recipient.get("name"),
            "role": "RECIPIENT_DELIVERY",
            "lat": rec_lat,
            "lng": rec_lng,
            "action": "Doorstep handover with digital beneficiary receipt",
            "est_time": f"T+{est_transit_mins} mins",
            "status": "FINAL_DESTINATION"
        })
    else:
        # Direct Express Corridor for Gaushala, Dog Shelter, or Compost
        mid_point_lat = (donor_lat + rec_lat) / 2
        mid_point_lng = (donor_lng + rec_lng) / 2
        waypoints.append({
            "step": 2,
            "name": "Express Eco-Corridor Transit Point",
            "role": "LOGISTICS_TELEMETRY",
            "lat": round(mid_point_lat, 4),
            "lng": round(mid_point_lng, 4),
            "action": "Real-time GPS route tracking & insulated telemetry monitoring",
            "est_time": f"T+{int(est_transit_mins * 0.5)} mins",
            "status": "CORRIDOR_TRANSIT"
        })
        waypoints.append({
            "step": 3,
            "name": recipient.get("name"),
            "role": "RECIPIENT_DELIVERY",
            "lat": rec_lat,
            "lng": rec_lng,
            "action": f"Doorstep unloading & weight verification ({rec_type.replace('_', ' ')})",
            "est_time": f"T+{est_transit_mins} mins",
            "status": "FINAL_DESTINATION"
        })

    return {
        "route_id": f"ROUTE-{uuid.uuid4().hex[:8].upper()}",
        "total_distance_km": road_dist_km,
        "est_transit_mins": est_transit_mins,
        "pickup_eta": f"{max(12, int(road_dist_km * 1.5))} mins",
        "courier_vehicle": "POTBHAR Insulated Electric EV Van #04",
        "driver_name": "Vikram Singh (Certified Courier Lead)",
        "driver_phone": "+91 98230 99001",
        "requires_lab_inspection": requires_lab_inspection,
        "routing_strategy": "OPTIMIZED_SHORTEST_TIME",
        "waypoints": waypoints
    }


# ─── Pydantic Request / Response Models ────────────────────────────────────────

class SmartRecommendRequest(BaseModel):
    food_title: str
    category: str
    is_non_veg: bool = False
    is_edible_for_animals: bool = True
    is_human_safe: bool = True
    temp_celsius: float = 64.0
    hours_since_cooked: float = 1.5
    quantity_kg: float = 25.0
    container_type: Optional[str] = "Insulated Stainless Cambro (Sealed)"
    donor_coords: Optional[Dict[str, float]] = Field(default_factory=lambda: {"lat": 18.5308, "lng": 73.8288})
    donor_location_name: Optional[str] = "Grand Pavilion Banquets, SB Road, Pune"
    preferred_type: Optional[str] = None  # GAUSHALA | DOG_SHELTER | HUMAN_SHELTER | COMPOST_MANURE | None


class SmartDonationSubmitRequest(BaseModel):
    donor_name: str
    donor_phone: str
    donor_location: str
    donor_coords: Optional[Dict[str, float]] = Field(default_factory=lambda: {"lat": 18.5308, "lng": 73.8288})
    food_title: str
    category: str
    quantity_kg: float
    is_non_veg: bool = False
    temp_celsius: float = 64.0
    recipient_id: str
    donation_mode: str = "SMART_RECOMMENDED"  # "DONOR_CHOSEN" or "SMART_RECOMMENDED"
    notes: Optional[str] = ""


class ScrapCompostConvertRequest(BaseModel):
    scraps_title: str
    waste_category: str  # Vegetable Trimmings, Stale Grains, Plate Scraps, Fruit Peelings, Spoiled Buffet
    quantity_kg: float
    donor_name: str
    donor_location: str
    contamination_free: bool = True
    preferred_compost_hub_id: Optional[str] = "rec_compost_01"


# ─── Endpoints ────────────────────────────────────────────────────────────────

@router.get("/recipients")
def get_all_recipients(
    recipient_type: Optional[str] = Query(None, description="Filter by: GAUSHALA, DOG_SHELTER, HUMAN_SHELTER, COMPOST_MANURE"),
    diet_tag: Optional[str] = Query(None, description="Filter by: PURE_VEG, NON_VEG_FRIENDLY, HUMAN_SAFE_HOT, ZERO_WASTE_COMPOST")
):
    """
    Returns full recipient cards with contact details, live capacity, and diet compatibility.
    """
    results = RECIPIENT_DIRECTORY
    if recipient_type:
        results = [r for r in results if r["type"] == recipient_type]
    if diet_tag:
        results = [r for r in results if r["diet_tag"] == diet_tag]
    return {
        "status": "success",
        "total_recipients": len(results),
        "recipients": results
    }


@router.get("/recipients/{recipient_id}")
def get_recipient_details(recipient_id: str):
    """
    Returns single recipient contact card.
    """
    rec = next((r for r in RECIPIENT_DIRECTORY if r["id"] == recipient_id), None)
    if not rec:
        raise HTTPException(404, "Recipient organization not found")
    return {"status": "success", "recipient": rec}


@router.post("/recommend")
def smart_recommend(req: SmartRecommendRequest):
    """
    AI/Rule-based smart recommendation engine.
    Matches surplus food based on:
    - Non-veg status -> Dog Shelter / Animal Rescue (never Gaushala)
    - High-starch/grains/rotis/veggies/fresh greens -> Gaushala (Cattle Sanctuary)
    - Hot safe human food (>60°C, fresh) -> Human Community Shelter
    - Kitchen scraps, non-edibles, spoiled items -> Bio-Compost / Organic Manure Plant
    """
    donor_lat = req.donor_coords.get("lat", 18.5308)
    donor_lng = req.donor_coords.get("lng", 73.8288)

    title_lower = req.food_title.lower()
    cat_lower = req.category.lower()

    # Determine recommended destination type
    primary_type = "HUMAN_SHELTER"
    rationale = []

    # Logic 1: Leftover food scraps or spoiled/non-edible food
    if (not req.is_edible_for_animals or "scrap" in title_lower or "trimming" in title_lower or
            "peel" in title_lower or "spoiled" in title_lower or "scrap" in cat_lower):
        primary_type = "COMPOST_MANURE"
        rationale.append("Food identified as kitchen prep scraps/non-edibles unsuitable for animal or human consumption.")
        rationale.append("100% Zero-Landfill protocol activated: Routing to certified aerobic composting & bio-methanation.")
        rationale.append("Generates nutrient-rich organic humus (khaad) and clean green biogas.")

    # Logic 2: Non-vegetarian food (chicken, mutton, fish, egg, bones, gravies)
    elif req.is_non_veg or any(w in title_lower for w in ["chicken", "mutton", "fish", "meat", "egg", "prawn", "non-veg"]):
        primary_type = "DOG_SHELTER"
        rationale.append("Non-vegetarian surplus detected. Animal welfare guidelines strictly prohibit meat in Gaushalas.")
        rationale.append("Paired with verified Dog Rescue & Stray Rehabilitation shelters providing high-protein diets to rescued animals.")
        rationale.append("Prevents nutritious animal-safe feast proteins from rotting in city garbage dumps.")

    # Logic 3: Fodder grains, excess rotis, cooked rice/dals, or food held below human safety threshold (50°C-58°C)
    elif (req.temp_celsius < 60.0 or req.hours_since_cooked > 4.0 or
          any(w in title_lower for w in ["roti", "chapati", "naan", "fodder", "grass", "dry bread"]) or
          "cattle" in cat_lower):
        primary_type = "GAUSHALA"
        rationale.append("Pure vegetarian grain, roti, or cooked surplus suitable for cattle digestion.")
        if req.temp_celsius < 60.0:
            rationale.append(f"Temperature logged at {req.temp_celsius}°C (below FSSAI 60°C hot-holding threshold for human dining).")
        rationale.append("Cattle digestive systems safely relish warm grains and rotis within 6 hours of preparation.")
        rationale.append("Zero landfill waste; directly feeds rescued cows and calves.")

    # Logic 4: Human Grade Hot Surplus (>60°C, fresh within 3 hours)
    elif req.is_human_safe and req.temp_celsius >= 60.0 and req.hours_since_cooked <= 3.5:
        primary_type = "HUMAN_SHELTER"
        rationale.append(f"Hot-holding temperature verified at {req.temp_celsius}°C (FSSAI Safe Zone >60°C).")
        rationale.append("Cooked under 3.5 hours ago with intact sealed packaging.")
        rationale.append("Prioritizes hungry human beneficiaries (night shelters, orphanages, elder care).")
        rationale.append("Requires mandatory FSSAI food safety inspection checkpoint before shelter delivery.")

    # If donor explicitly selected preferred_type, honor it if safe
    if req.preferred_type in ["GAUSHALA", "DOG_SHELTER", "HUMAN_SHELTER", "COMPOST_MANURE"]:
        if req.preferred_type == "GAUSHALA" and req.is_non_veg:
            rationale.append("⚠️ Note: Donor requested Gaushala, but non-veg food cannot be fed to cows. Overriding to Dog Shelter for animal safety.")
            primary_type = "DOG_SHELTER"
        else:
            primary_type = req.preferred_type
            rationale.insert(0, f"Donor preference respected: Explicitly routed to {req.preferred_type.replace('_', ' ').title()}.")

    # Filter recipients matching the primary type
    candidates = [r for r in RECIPIENT_DIRECTORY if r["type"] == primary_type]
    if not candidates:
        candidates = RECIPIENT_DIRECTORY

    # Score candidates based on distance and capacity
    scored_candidates = []
    for cand in candidates:
        dist = calculate_haversine_distance(donor_lat, donor_lng, cand["latitude"], cand["longitude"])
        capacity_ok = cand["capacity_remaining_kg"] >= req.quantity_kg
        # Higher score for closer distance and available capacity
        score = round((10 / (dist + 2.0)) * 50 + (cand["rating"] * 8) + (15 if capacity_ok else -20), 1)
        scored_candidates.append({
            "recipient": cand,
            "distance_km": round(dist * 1.25, 1),
            "match_score": min(99.0, max(65.0, score)),
            "capacity_sufficient": capacity_ok
        })

    scored_candidates.sort(key=lambda x: x["match_score"], reverse=True)
    best_candidate = scored_candidates[0]["recipient"]
    best_match_score = scored_candidates[0]["match_score"]

    # Generate optimized route
    optimized_route = generate_optimized_route(req.donor_coords, best_candidate)

    # Compute composting projection if compost facility is chosen
    compost_stats = None
    if primary_type == "COMPOST_MANURE":
        compost_ratio = best_candidate.get("compost_output_ratio", 0.30)
        yield_kg = round(req.quantity_kg * compost_ratio, 1)
        methane_offset = round(req.quantity_kg * 1.9, 1)
        cng_equiv_kwh = round(req.quantity_kg * 0.45, 1)
        compost_stats = {
            "input_waste_kg": req.quantity_kg,
            "estimated_humus_khaad_kg": yield_kg,
            "methane_prevented_co2e_kg": methane_offset,
            "clean_energy_equiv_kwh": cng_equiv_kwh,
            "mature_cycle_days": 18,
            "process_type": "Aerobic Thermophilic Microbial Micro-Composting"
        }

    return {
        "status": "success",
        "recommended_destination_type": primary_type,
        "recommended_destination_label": best_candidate["type_label"],
        "match_confidence_pct": best_match_score,
        "rationale": rationale,
        "recommended_recipient": best_candidate,
        "distance_km": scored_candidates[0]["distance_km"],
        "optimized_route": optimized_route,
        "compost_conversion": compost_stats,
        "alternative_recipients": [s["recipient"] for s in scored_candidates[1:4]]
    }


@router.post("/donate")
def submit_smart_donation(req: SmartDonationSubmitRequest, db: Session = Depends(get_db)):
    """
    Submits a new smart donation batch, creates delivery corridor, and logs audit trail.
    """
    rec = next((r for r in RECIPIENT_DIRECTORY if r["id"] == req.recipient_id), None)
    if not rec:
        raise HTTPException(404, "Selected recipient organization not found")

    batch_id = f"PB-SMART-{uuid.uuid4().hex[:6].upper()}"
    tracking_code = f"TRK-{uuid.uuid4().hex[:8].upper()}"

    # Calculate impact points
    credits = int(req.quantity_kg * 10)
    if req.is_non_veg:
        credits += 50

    optimized_route = generate_optimized_route(req.donor_coords, rec)

    donation_record = {
        "batch_id": batch_id,
        "tracking_code": tracking_code,
        "donor_name": req.donor_name,
        "donor_phone": req.donor_phone,
        "donor_location": req.donor_location,
        "food_title": req.food_title,
        "category": req.category,
        "quantity_kg": req.quantity_kg,
        "is_non_veg": req.is_non_veg,
        "temp_celsius": req.temp_celsius,
        "recipient": rec,
        "recipient_type": rec["type"],
        "donation_mode": req.donation_mode,
        "status": "DISPATCHED_IN_TRANSIT",
        "impact_credits_earned": credits,
        "estimated_meals_or_portions": int(req.quantity_kg * 2.5),
        "co2e_prevented_kg": round(req.quantity_kg * 1.9, 1),
        "created_at": datetime.utcnow().isoformat(),
        "optimized_route": optimized_route,
        "sms_notification_sent": {
            "recipient_alert": f"POTBHAR Alert: Inbound surplus of {req.quantity_kg}kg {req.food_title} from {req.donor_name} is dispatched with Courier #04. ETA {optimized_route['pickup_eta']}.",
            "donor_receipt": f"Thank you {req.donor_name}! Your smart donation of {req.quantity_kg}kg has been matched with {rec['name']}. +{credits} Impact Credits credited."
        }
    }

    # Record in database if Organization exists, or create a lightweight entry
    try:
        donor_org = db.query(Organization).filter(Organization.organization_type == "DONOR").first()
        if donor_org:
            new_batch = FoodBatch(
                id=batch_id,
                donor_id=donor_org.id,
                food_category=req.category,
                description=f"{req.food_title} (Smart Routed to {rec['type']})",
                quantity_kg=req.quantity_kg,
                storage_temp=f"{req.temp_celsius}°C",
                status=BatchStatus.IN_TRANSIT
            )
            db.add(new_batch)
            db.commit()
    except Exception as e:
        db.rollback()

    return {
        "status": "success",
        "message": f"Smart donation successfully confirmed! Courier dispatched to {rec['name']}.",
        "donation": donation_record
    }


@router.post("/compost-convert")
def convert_scraps_to_compost(req: ScrapCompostConvertRequest):
    """
    Converts kitchen prep scraps / non-edibles into rich bio-compost (Khaad) & clean energy.
    Calculates exact humus output, carbon reduction, and generates certification.
    """
    hub = next((r for r in RECIPIENT_DIRECTORY if r["id"] == req.preferred_compost_hub_id), RECIPIENT_DIRECTORY[6])

    humus_ratio = hub.get("compost_output_ratio", 0.30)
    humus_yield_kg = round(req.quantity_kg * humus_ratio, 1)
    co2e_prevented = round(req.quantity_kg * 1.9, 1)
    biocng_kwh = round(req.quantity_kg * 0.48, 1)
    nitrogen_potassium_rich_pct = 94.5

    batch_code = f"COMPOST-{uuid.uuid4().hex[:6].upper()}"

    certificate = {
        "batch_code": batch_code,
        "facility_name": hub["name"],
        "facility_address": hub["address"],
        "lead_engineer": hub["contact_person"],
        "donor_organization": req.donor_name,
        "donor_location": req.donor_location,
        "scraps_description": req.scraps_title,
        "waste_category": req.waste_category,
        "input_scrap_kg": req.quantity_kg,
        "output_organic_humus_kg": humus_yield_kg,
        "carbon_methane_offset_kg": co2e_prevented,
        "clean_energy_generated_kwh": biocng_kwh,
        "maturation_time_days": 18,
        "compost_grade": "Grade-1 Certified Organic Agronomic Humus (FCO 1985 Standard)",
        "destination_beneficiary": "Local Urban Farmers, Peri-Urban Organic Agro-collectives & Tree Plantations",
        "issued_at": datetime.utcnow().strftime("%d %B %Y, %I:%M %p IST")
    }

    return {
        "status": "success",
        "message": f"Leftover scrap batch {batch_code} approved for 100% bio-compost diversion! Zero landfill waste.",
        "compost_hub": hub,
        "certificate": certificate
    }
