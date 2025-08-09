from fastapi import APIRouter, Depends, HTTPException, Body
from typing import List
from fastapi.security import OAuth2PasswordBearer
from ..config import supabase
from ..models import DietEntry, MealEntry
import jwt
from datetime import datetime, date
from uuid import UUID
from pydantic import BaseModel

router = APIRouter(prefix="/health", tags=["health"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


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
    child_id = supabase.table("students").select(
        "student_id").eq("email", email).execute()
    res = supabase.table("meals").select("id, time, mealtype, description, calories, proteins, carbs, fat").eq(
        "student_id", child_id.data[0]['student_id']).order("time", desc=True).execute()
    return res.data


@router.post("/meals", response_model=dict)
def log_meal(data: MealEntry, email: str = Depends(get_user_email_from_token)):
    child_id = supabase.table("students").select(
        "student_id").eq("email", email).execute()
    supabase.table("meals").insert({
        "student_id": child_id.data[0]['student_id'],
        "time": datetime.now().isoformat(),
        "mealtype": data.mealtype,
        "description": data.description,
        "calories": data.calories,
        "proteins": data.proteins,
        "carbs": data.carbs,
        "fat": data.fat,
    }).execute()
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
