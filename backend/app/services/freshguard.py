"""
FreshGuard AI Service - Rules-based food quality risk assessment
Vision analysis simulation + structured risk evaluation
"""
import math
from datetime import datetime
from typing import Optional


COOKED_FOOD_CATEGORIES = [
    "cooked_rice", "curry", "dal", "biryani", "roti", "bread",
    "cooked_vegetables", "meat_dishes", "soup", "stew", "prepared_meals"
]

RAW_FOOD_CATEGORIES = [
    "raw_vegetables", "fruits", "raw_meat", "dairy", "eggs"
]

SAFE_HOURS_ROOM_TEMP = {
    "cooked_rice": 4, "curry": 4, "dal": 4, "biryani": 4,
    "roti": 6, "bread": 12, "cooked_vegetables": 4,
    "meat_dishes": 2, "soup": 4, "stew": 4,
    "prepared_meals": 4, "raw_vegetables": 8, "fruits": 24,
    "raw_meat": 2, "dairy": 2, "eggs": 24
}

SAFE_HOURS_CHILLED = {
    "cooked_rice": 24, "curry": 48, "dal": 48, "biryani": 24,
    "roti": 48, "bread": 72, "cooked_vegetables": 48,
    "meat_dishes": 48, "soup": 72, "stew": 72,
    "prepared_meals": 24, "raw_vegetables": 72, "fruits": 120,
    "raw_meat": 48, "dairy": 48, "eggs": 168
}


def analyze_image(food_category: str, image_path: Optional[str] = None) -> dict:
    """
    Simulated FreshGuard Vision analysis.
    In production: run actual CNN inference on the uploaded image.
    For demo: returns a realistic rules-based assessment.
    """
    # Simulate model output based on category
    base_confidence = 0.82 + (hash(food_category or "unknown") % 10) / 100

    return {
        "model_name": "FreshGuard-Vision",
        "model_version": "1.0.0",
        "assessment_method": "SIMULATED_VISION",
        "prediction_target": "visible_quality_classification",
        "predicted_class": "NO_OBVIOUS_VISIBLE_DEFECT",
        "class_probabilities": {
            "VISIBLE_DETERIORATION": round(0.06 - (base_confidence - 0.76) * 0.1, 3),
            "OTHER_VISIBLE_DEFECT": round(0.08, 3),
            "NO_OBVIOUS_VISIBLE_DEFECT": round(base_confidence, 3),
            "IMAGE_UNSUITABLE": 0.02,
            "UNCERTAIN": 0.02
        },
        "confidence": round(base_confidence, 3),
        "requires_human_review": base_confidence < 0.70,
        "is_food_safety_certification": False,
        "assessment_note": (
            "No visible deterioration detected in uploaded photograph. "
            "This visual assessment does not certify food safety. "
            "Structured quality risk assessment and human assessor review are required "
            "before any redistribution decision."
        )
    }


def evaluate_quality_risk(
    food_category: str,
    preparation_time: Optional[datetime],
    storage_temp: str,
    storage_method: Optional[str],
    packaging_intact: Optional[bool],
    handling_completeness: float,
    transport_duration_hours: float = 0
) -> dict:
    """
    FreshGuard Risk — Rules-based quality risk screening.
    Transparent, documented, FSSAI-informed thresholds.
    """
    risk_flags = []
    contributing_factors = []

    # Time-based checks
    if preparation_time:
        hours_since_prep = (datetime.utcnow() - preparation_time).total_seconds() / 3600
        hours_since_prep += transport_duration_hours
        cat_key = food_category.lower().replace(" ", "_")

        safe_room = SAFE_HOURS_ROOM_TEMP.get(cat_key, 4)
        safe_chilled = SAFE_HOURS_CHILLED.get(cat_key, 24)

        if storage_temp == "ROOM_TEMP":
            if hours_since_prep > safe_room:
                risk_flags.append({
                    "flag": "DANGER_ZONE_EXCEEDED",
                    "detail": f"Food at room temperature for {hours_since_prep:.1f}h (limit: {safe_room}h)"
                })
            elif hours_since_prep > safe_room * 0.75:
                contributing_factors.append("approaching_room_temp_limit")
        elif storage_temp in ("CHILLED", "REFRIGERATED"):
            if hours_since_prep > safe_chilled:
                risk_flags.append({
                    "flag": "EXTENDED_CHILLED_STORAGE",
                    "detail": f"Chilled storage {hours_since_prep:.1f}h (limit: {safe_chilled}h)"
                })
            else:
                contributing_factors.append("adequate_chilled_storage")
        elif storage_temp == "FROZEN":
            contributing_factors.append("frozen_storage_adequate")
    else:
        risk_flags.append({
            "flag": "PREPARATION_TIME_UNKNOWN",
            "detail": "Preparation time not provided; cannot assess time-based risk"
        })

    # Handling history completeness
    if handling_completeness < 0.5:
        risk_flags.append({
            "flag": "INCOMPLETE_HANDLING_HISTORY",
            "detail": f"Handling history {int(handling_completeness * 100)}% complete (required: 70%+)"
        })
    elif handling_completeness < 0.7:
        contributing_factors.append("partial_handling_history")
    else:
        contributing_factors.append("adequate_handling_documentation")

    # Packaging integrity
    if packaging_intact is False:
        risk_flags.append({
            "flag": "COMPROMISED_PACKAGING",
            "detail": "Packaging reported as compromised or broken"
        })
    elif packaging_intact is True:
        contributing_factors.append("intact_packaging")

    # Storage method
    if storage_method in ("OPEN", "UNCOVERED"):
        risk_flags.append({
            "flag": "OPEN_STORAGE",
            "detail": "Food stored in open container increases contamination risk"
        })
    elif storage_method in ("SEALED", "VACUUM_PACKED"):
        contributing_factors.append("sealed_storage")

    risk_level = "ELEVATED" if risk_flags else "STANDARD"

    return {
        "model_name": "FreshGuard-Risk",
        "model_version": "1.0.0",
        "assessment_method": "RULES_BASED",
        "prediction_target": "quality_deterioration_risk",
        "prediction_available": True,
        "risk_category": risk_level,
        "risk_flags": risk_flags,
        "contributing_factors": contributing_factors,
        "requires_assessor_review": len(risk_flags) > 0,
        "is_food_safety_certification": False,
        "assessment_note": (
            "This is a rules-based quality risk screening. It is NOT a food-safety certificate. "
            "An authorized assessor must review all batches before redistribution approval."
        )
    }


def run_safety_engine(batch) -> dict:
    """
    Safety engine decision logic.
    Returns recommended status and reasons.
    """
    flags = []

    # Check preparation time for cooked foods
    cat_lower = (batch.food_category or "").lower().replace(" ", "_")
    if cat_lower in COOKED_FOOD_CATEGORIES and not batch.preparation_time:
        flags.append("MISSING_PREPARATION_TIME_FOR_COOKED_FOOD")

    # Check minimum quantity
    if batch.quantity_kg <= 0:
        flags.append("INVALID_QUANTITY")

    # Completeness check
    if batch.handling_completeness < 0.5:
        flags.append("INSUFFICIENT_HANDLING_DATA")

    if flags:
        return {
            "recommended_status": "PENDING_INFORMATION",
            "flags": flags,
            "can_proceed_to_matching": False
        }

    return {
        "recommended_status": "ASSESSMENT_REQUIRED",
        "flags": [],
        "can_proceed_to_matching": False  # Always requires human assessor
    }


def match_recipients(batch, recipients, donor_lat=None, donor_lon=None) -> list:
    """
    Intelligent recipient matching with weighted scoring.
    """
    scored = []
    for req in recipients:
        # Hard filter: category match
        if req.food_category.lower() != batch.food_category.lower():
            continue

        # Hard filter: capacity
        if req.capacity_kg < 1.0:
            continue

        # Calculate distance (Haversine if coords available)
        distance_km = 5.0  # default
        org = req.recipient
        if org and org.latitude and org.longitude and donor_lat and donor_lon:
            distance_km = haversine(donor_lat, donor_lon, org.latitude, org.longitude)

        if distance_km > 50:
            continue  # Too far

        # Weighted score
        proximity_score = 1 / (distance_km + 1)
        capacity_score = min(req.capacity_kg / 100, 1.0)
        urgency_score = min(req.quantity_needed_kg / 50, 1.0)

        score = (0.40 * proximity_score + 0.35 * urgency_score + 0.25 * capacity_score)

        scored.append({
            "requirement": req,
            "organization": org,
            "estimated_distance_km": round(distance_km, 2),
            "match_score": round(score, 4)
        })

    return sorted(scored, key=lambda x: x["match_score"], reverse=True)


def haversine(lat1, lon1, lat2, lon2) -> float:
    R = 6371
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
