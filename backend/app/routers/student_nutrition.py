from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.security import OAuth2PasswordBearer
from typing import Any, Dict, List, Optional, Tuple
from datetime import date, datetime, timedelta
from uuid import UUID
import os
import json
import jwt

from ..config import supabase
from google import genai
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/health", tags=["health"])  # keep under /health like other student_* routers
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

_gemini_client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
_GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


# -------------------------
# Helpers
# -------------------------

def get_user_email_from_token(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = jwt.decode(token, options={"verify_signature": False})
        email = payload.get("email")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        return email
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


def _get_student_id_and_grade(email: str) -> Tuple[str, Optional[str]]:
    res = (
        supabase
        .table("students")
        .select("student_id, grade_level")
        .eq("email", email)
        .single()
        .execute()
    )
    if not res.data:
        raise HTTPException(status_code=404, detail="Student not found")
    return res.data["student_id"], res.data.get("grade_level")


def _date_range_bounds(range_key: str) -> Tuple[str, str]:
    # returns ISO dates for inclusive start and exclusive end bounds as strings with time
    today = date.today()
    if range_key == "today":
        start = today
        end = today + timedelta(days=1)
    elif range_key == "7d":
        start = today - timedelta(days=6)
        end = today + timedelta(days=1)
    elif range_key == "30d":
        start = today - timedelta(days=29)
        end = today + timedelta(days=1)
    else:
        start = today
        end = today + timedelta(days=1)
    return f"{start.isoformat()} 00:00:00", f"{end.isoformat()} 00:00:00"


# -------------------------
# Data aggregation
# -------------------------

def _fetch_meals(student_id: str, start_dt: str, end_dt: str) -> List[Dict[str, Any]]:
    res = (
        supabase.table("meals")
        .select("id, time, mealtype, description, calories, proteins, carbs, fat, sodium, sugar")
        .eq("student_id", student_id)
        .gte("time", start_dt)
        .lt("time", end_dt)
        .order("time", desc=True)
        .execute()
    )
    return res.data or []


def _fetch_water(student_id: str, start_dt: str, end_dt: str) -> List[Dict[str, Any]]:
    # water_intake has separate intake_date and time; filter by date range
    start_date = start_dt.split(" ")[0]
    end_date = (datetime.fromisoformat(end_dt.replace(" ", "T")).date())
    # Collect all days in [start_date, end_date)
    res = (
        supabase.table("water_intake")
        .select("intake_id, amount_ml, container_type, intake_time, intake_date")
        .eq("user_id", student_id)
        .gte("intake_date", start_date)
        .lt("intake_date", end_date.isoformat())
        .order("intake_date")
        .execute()
    )
    return res.data or []


def _fetch_latest_metrics(student_id: str) -> Optional[Dict[str, Any]]:
    res = (
        supabase.table("health_metrics")
        .select("created_at, weight, height, bmi, systolic, diastolic, blood_sugar, heart_rate, notes, age_years, sex")
        .eq("student_id", student_id)
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )
    return (res.data or [None])[0]


def _fetch_conditions(student_id: str) -> List[Dict[str, Any]]:
    res = (
        supabase.table("health_conditions")
        .select("condition_id, condition_name, severity, dietary_restrictions, is_active, diagnosed_date")
        .eq("user_id", student_id)
        .eq("is_active", True)
        .order("created_at", desc=True)
        .execute()
    )
    return res.data or []


def _fetch_medications_and_logs(student_id: str, start_dt: str, end_dt: str) -> Dict[str, Any]:
    meds = (
        supabase.table("medications")
        .select("medication_id, medication_name, dosage, frequency, start_date, end_date")
        .eq("user_id", student_id)
        .order("created_at", desc=True)
        .execute()
    ).data or []
    # logs within window
    logs = (
        supabase.table("medication_logs")
        .select("log_id, medication_id, taken_at, quantity_taken, notes")
        .eq("user_id", student_id)
        .gte("taken_at", start_dt)
        .lt("taken_at", end_dt)
        .order("taken_at", desc=True)
        .execute()
    ).data or []
    return {"medications": meds, "logs": logs}


# removed grade-based age estimation; rely on age_years provided in health_metrics


# -------------------------
# Gemini
# -------------------------

def _call_gemini(inputs_snapshot: Dict[str, Any]) -> Dict[str, Any]:
    response_schema = {
        "type": "object",
        "properties": {
            "overview": {"type": "string"},
            "risks": {"type": "array", "items": {"type": "string"}},
            "macro_targets": {
                "type": "object",
                "properties": {
                    "calories": {"type": "number"},
                    "proteins": {"type": "number"},
                    "carbs": {"type": "number"},
                    "fat": {"type": "number"},
                    "sodium": {"type": "number"},
                    "sugar": {"type": "number"},
                },
            },
            "hydration_advice": {"type": "string"},
            "alerts": {"type": "array", "items": {"type": "string"}},
            "meal_plan": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "timeOfDay": {"type": "string"},
                        "item": {"type": "string"},
                        "rationale": {"type": "string"},
                    },
                },
            },
            "notes": {"type": "string"},
        },
    }

    prompt = (
        "You are a child-safe nutrition assistant. Generate concise, actionable diet and hydration suggestions "
        "based on the provided user data. Avoid medical diagnosis; give general wellness guidance and respect "
        "dietary restrictions.")

    contents = [
        {"role": "user", "parts": [{"text": (
            f"Context (JSON):\n" + json.dumps(inputs_snapshot, ensure_ascii=False, default=str) +
            "\nReturn structured JSON only per the schema."
        )}]}
    ]

    try:
        resp = _gemini_client.models.generate_content(
            model=_GEMINI_MODEL,
            contents=contents,
            config={
                "response_mime_type": "application/json",
                "response_schema": response_schema,
            },
        )
        data = json.loads(resp.text)
        # minimal validation
        if not isinstance(data, dict):
            raise ValueError("Invalid Gemini output")
        return data
    except Exception as e:
        print(f"Gemini suggestions generation failed: {e}")
        return {
            "overview": "Could not generate suggestions at this time.",
            "risks": [],
            "macro_targets": {"calories": 0, "proteins": 0, "carbs": 0, "fat": 0, "sodium": 0, "sugar": 0},
            "hydration_advice": "",
            "alerts": [],
            "meal_plan": [],
            "notes": "",
        }


# -------------------------
# Endpoints
# -------------------------

@router.post("/nutrition/suggestions/generate", response_model=dict)
def generate_suggestions(range: str = Query("today", pattern="^(today|7d|30d)$"), email: str = Depends(get_user_email_from_token)):
    student_id, grade_level = _get_student_id_and_grade(email)
    start_dt, end_dt = _date_range_bounds(range)

    meals = _fetch_meals(student_id, start_dt, end_dt)
    water = _fetch_water(student_id, start_dt, end_dt)
    metrics = _fetch_latest_metrics(student_id)
    conditions = _fetch_conditions(student_id)
    meds = _fetch_medications_and_logs(student_id, start_dt, end_dt)

    # derive demographics from latest metrics if available
    age_years = None
    sex = None
    if metrics:
        age_years = metrics.get("age_years")
        sex = metrics.get("sex")

    # rollups
    total_cal = sum(float(m.get("calories") or 0) for m in meals)
    total_pro = sum(float(m.get("proteins") or 0) for m in meals)
    total_carb = sum(float(m.get("carbs") or 0) for m in meals)
    total_fat = sum(float(m.get("fat") or 0) for m in meals)
    total_sodium = sum(float(m.get("sodium") or 0) for m in meals)
    total_sugar = sum(float(m.get("sugar") or 0) for m in meals)
    total_water_ml = sum(int(w.get("amount_ml") or 0) for w in water)

    snapshot: Dict[str, Any] = {
        "range": range,
        "student": {
            "student_id": student_id,
            "age_years": age_years,
            "sex": sex,
        },
        "metrics_latest": metrics,
        "conditions_active": conditions,
        "medications": meds.get("medications", []),
        "medication_logs": meds.get("logs", []),
        "meals_rollup": {
            "calories": total_cal,
            "proteins": total_pro,
            "carbs": total_carb,
            "fat": total_fat,
            "sodium": total_sodium,
            "sugar": total_sugar,
        },
        "meals_examples": [
            {
                "time": m.get("time"),
                "mealtype": m.get("mealtype"),
                "description": m.get("description"),
                "calories": m.get("calories"),
                "sodium": m.get("sodium"),
                "sugar": m.get("sugar"),
            }
            for m in meals[:8]
        ],
        "water_total_ml": total_water_ml,
        "water_days": list({w.get("intake_date") for w in water if w.get("intake_date")}),
        "generated_at": datetime.now().isoformat(),
    }

    suggestions = _call_gemini(snapshot)

    # persist suggestions
    rec = {
        "user_id": student_id,
        "generated_at": datetime.now().isoformat(),
        "range_key": range,
        "model": _GEMINI_MODEL,
        "inputs_snapshot": snapshot,
        "suggestions": suggestions,
    }
    try:
        saved = supabase.table("nutrition_suggestions").insert(rec).execute()
        saved_row = (saved.data or [rec])[0]
    except Exception as e:
        # do not fail generation; return response even if saving fails
        print(f"Failed to save nutrition_suggestions: {e}")
        saved_row = rec

    return saved_row


@router.get("/nutrition/suggestions/latest", response_model=dict)
def latest_suggestions(range: str = Query("today", pattern="^(today|7d|30d)$"), email: str = Depends(get_user_email_from_token)):
    student_id, _ = _get_student_id_and_grade(email)
    res = (
        supabase.table("nutrition_suggestions")
        .select("*")
        .eq("user_id", student_id)
        .eq("range_key", range)
        .order("generated_at", desc=True)
        .limit(1)
        .execute()
    )
    if not res.data:
        raise HTTPException(status_code=404, detail="No suggestions found")
    return res.data[0]


@router.get("/nutrition/suggestions", response_model=List[dict])
def list_suggestions(limit: int = Query(10, ge=1, le=50), email: str = Depends(get_user_email_from_token)):
    student_id, _ = _get_student_id_and_grade(email)
    res = (
        supabase.table("nutrition_suggestions")
        .select("*")
        .eq("user_id", student_id)
        .order("generated_at", desc=True)
        .limit(limit)
        .execute()
    )
    return res.data or []
