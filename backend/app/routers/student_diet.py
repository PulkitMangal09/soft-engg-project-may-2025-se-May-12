from fastapi import APIRouter, Depends, HTTPException, Body
from typing import List
from fastapi.security import OAuth2PasswordBearer
from ..config import supabase
from ..models import DietEntry, MealEntry, MealCreate
from google import genai
import os
import json
from dotenv import load_dotenv
import jwt
from datetime import datetime, date
from uuid import UUID
from pydantic import BaseModel

router = APIRouter(prefix="/health", tags=["health"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

load_dotenv()
_gemini_client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
_gemini_model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")


def estimate_nutrition_with_gemini(description: str) -> dict:
    """Call Gemini to estimate nutrition. Returns dict with calories, proteins, carbs, fat (numbers)."""
    response_schema = {
        "type": "object",
        "properties": {
            "calories": {"type": "number"},
            "proteins": {"type": "number"},
            "carbs": {"type": "number"},
            "fat": {"type": "number"},
        },
        "required": ["calories", "proteins", "carbs", "fat"],
    }
    prompt = (
        "Estimate macronutrients for the following food description. "
        "Return strict JSON with numeric fields: calories (kcal), proteins (g), carbs (g), fat (g).\n\n"
        f"Food: {description}"
    )
    try:
        resp = _gemini_client.models.generate_content(
            model=_gemini_model,
            contents=[{"role": "user", "parts": [{"text": prompt}]}],
            config={
                "response_mime_type": "application/json",
                "response_schema": response_schema,
            },
        )
        data = json.loads(resp.text)
        # Basic sanitation to ensure numbers
        def n(v):
            try:
                return float(v)
            except Exception:
                return 0.0
        return {
            "calories": n(data.get("calories")),
            "proteins": n(data.get("proteins")),
            "carbs": n(data.get("carbs")),
            "fat": n(data.get("fat")),
        }
    except Exception as e:
        # Fallback to zeros on any failure
        print(f"Gemini nutrition estimate failed: {e}")
        return {"calories": 0.0, "proteins": 0.0, "carbs": 0.0, "fat": 0.0}

def get_user_email_from_token(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = jwt.decode(token, options={"verify_signature": False})
        return payload.get("email")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

# -------------------------
# Student Diet Endpoints
# -------------------------


@router.get("/student_diet", response_model=List[DietEntry])
def get_diet_logs(email: str = Depends(get_user_email_from_token)):
    child_id = supabase.table("students").select(
        "student_id").eq("email", email).execute()
    res = supabase.table("student_diet").select("id, time, water_glasses, sodium, sugar").eq(
        "student_id", child_id.data[0]['student_id']).order("time", desc=True).execute()
    return res.data


@router.post("/student_diet", response_model=dict)
def log_student_diet(data: DietEntry, email: str = Depends(get_user_email_from_token)):
    child_id = supabase.table("students").select(
        "student_id").eq("email", email).execute()
    supabase.table("student_diet").insert({
        "student_id": child_id.data[0]['student_id'],
        "time": datetime.now().isoformat(),
        "water_glasses": data.water_glasses,
        "sodium": data.sodium,
        "sugar": data.sugar,
    }).execute()
    return {"message": "Diet entry saved"}


@router.patch("/student_diet/{entry_id}", response_model=dict)
def update_diet_entry(
    entry_id: UUID,
    data: DietEntry,
    email: str = Depends(get_user_email_from_token)
):
    child_id = supabase.table("students").select(
        "student_id").eq("email", email).execute()
    response = supabase.table("student_diet").update({
        "water_glasses": data.water_glasses,
        "sodium": data.sodium,
        "sugar": data.sugar
    }).eq("id", entry_id).eq("student_id", child_id.data[0]['student_id']).execute()

    if not response.data:
        raise HTTPException(
            status_code=404, detail="Diet entry not found or unauthorized")

    return {"message": "Diet entry updated"}


@router.delete("/student_diet/{entry_id}", response_model=dict)
def delete_diet_entry(
    entry_id: UUID,
    email: str = Depends(get_user_email_from_token)
):
    child_id = supabase.table("students").select(
        "student_id").eq("email", email).execute()
    response = supabase.table("student_diet").delete().eq("id", entry_id).eq(
        "student_id", child_id.data[0]['student_id']).execute()

    if not response.data:
        raise HTTPException(
            status_code=404, detail="Diet entry not found or unauthorized")

    return {"message": "Diet entry deleted"}


# -------------------------
# Meals Logging Endpoints
# -------------------------
@router.get("/meals", response_model=List[MealEntry])
def get_meal_logs(email: str = Depends(get_user_email_from_token)):
    student_id = _get_student_id(email)
    today = date.today().isoformat()
    # Use half-open interval [today 00:00, tomorrow 00:00)
    # Construct tomorrow date string by adding one day
    from datetime import timedelta
    tomorrow = (date.today() + timedelta(days=1)).isoformat()
    res = (
        supabase.table("meals")
        .select("id, time, mealtype, description, calories, proteins, carbs, fat")
        .eq("student_id", student_id)
        .gte("time", f"{today} 00:00:00")
        .lt("time", f"{tomorrow} 00:00:00")
        .order("time", desc=True)
        .execute()
    )
    return res.data


@router.post("/meals", response_model=dict)
def log_meal(data: MealCreate, email: str = Depends(get_user_email_from_token)):
    student_id = _get_student_id(email)
    # Always recompute nutrition on backend using Gemini; ignore client-sent nutrient values
    nutrition = estimate_nutrition_with_gemini(data.description)
    payload = {
        "student_id": student_id,
        "time": datetime.now().isoformat(),
        "mealtype": data.mealtype,
        "description": data.description,
        "calories": nutrition.get("calories", 0.0),
        "proteins": nutrition.get("proteins", 0.0),
        "carbs": nutrition.get("carbs", 0.0),
        "fat": nutrition.get("fat", 0.0),
    }
    try:
        supabase.table("meals").insert(payload).execute()
    except Exception as e:
        # Surface a readable error back to the client
        raise HTTPException(status_code=500, detail=f"Failed to log meal: {e}")
    return {"message": "Meal entry saved"}


@router.patch("/meals/{entry_id}", response_model=dict)
def update_meal_entry(
    entry_id: UUID,
    data: MealEntry,
    email: str = Depends(get_user_email_from_token)
):
    child_id = supabase.table("students").select(
        "student_id").eq("email", email).execute()
    response = supabase.table("meals").update({
        "mealtype": data.mealtype,
        "description": data.description,
        "calories": data.calories,
        "proteins": data.proteins,
        "carbs": data.carbs,
        "fat": data.fat
    }).eq("id", entry_id).eq("student_id", child_id.data[0]['student_id']).execute()

    if not response.data:
        raise HTTPException(
            status_code=404, detail="Meal entry not found or unauthorized")

    return {"message": "Meal entry updated"}


@router.delete("/meals/{entry_id}", response_model=dict)
def delete_meal_entry(
    entry_id: UUID,
    email: str = Depends(get_user_email_from_token)
):
    child_id = supabase.table("students").select(
        "student_id").eq("email", email).execute()
    response = supabase.table("meals").delete().eq("id", entry_id).eq(
        "student_id", child_id.data[0]['student_id']).execute()

    if not response.data:
        raise HTTPException(
            status_code=404, detail="Meal entry not found or unauthorized")

    return {"message": "Meal entry deleted"}


# -------------------------
# Water Intake Endpoints
# -------------------------

class WaterIntakeCreate(BaseModel):
    amount_ml: int = 250
    container_type: str = "glass"
    intake_date: date | None = None
    intake_time: str | None = None


def _get_student_id(email: str) -> str:
    child = supabase.table("students").select(
        "student_id").eq("email", email).single().execute()
    if not child.data:
        raise HTTPException(status_code=404, detail="Student not found")
    return child.data["student_id"]


@router.get("/water/summary", response_model=dict)
def get_water_summary(email: str = Depends(get_user_email_from_token)):
    student_id = _get_student_id(email)
    today = date.today().isoformat()
    res = supabase.table("water_intake").select("amount_ml").eq(
        "user_id", student_id).eq("intake_date", today).execute()
    total_ml = sum((r.get("amount_ml") or 0) for r in (res.data or []))
    glasses = round(total_ml / 250) if total_ml else 0
    return {"total_ml": total_ml, "glasses": glasses}


@router.post("/water", response_model=dict)
def add_water_intake(data: WaterIntakeCreate = Body(default=None), email: str = Depends(get_user_email_from_token)):
    student_id = _get_student_id(email)
    payload = {
        "user_id": student_id,
        "amount_ml": (data.amount_ml if data else 250),
        "container_type": (data.container_type if data else "glass"),
        "intake_date": (data.intake_date.isoformat() if (data and data.intake_date) else date.today().isoformat()),
        # let DB default the time if not provided
    }
    supabase.table("water_intake").insert(payload).execute()
    # return updated summary
    return get_water_summary(email)


@router.get("/water/logs", response_model=List[dict])
def get_water_logs(email: str = Depends(get_user_email_from_token)):
    student_id = _get_student_id(email)
    today = date.today().isoformat()
    res = (
        supabase.table("water_intake")
        .select("intake_id, amount_ml, container_type, intake_time, intake_date, created_at")
        .eq("user_id", student_id)
        .eq("intake_date", today)
        .order("intake_time")
        .execute()
    )
    return res.data or []
