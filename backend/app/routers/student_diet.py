from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from fastapi.security import OAuth2PasswordBearer
from ..config import supabase
import jwt
from datetime import datetime

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
class DietEntry(BaseModel):
    water_glasses: int
    sodium: float
    sugar: float

@router.post("/student_diet", response_model=dict)
def log_student_diet(data: DietEntry, email: str = Depends(get_user_email_from_token)):
    supabase.table("student_diet").insert({
        "email": email,
        "time": datetime.now().isoformat(),
        "water_glasses": data.water_glasses,
        "sodium": data.sodium,
        "sugar": data.sugar,
    }).execute()
    return {"message": "Diet entry saved"}

@router.get("/student_diet", response_model=List[DietEntry])
def get_diet_logs(email: str = Depends(get_user_email_from_token)):
    res = supabase.table("student_diet").select("time, water_glasses, sodium, sugar").eq("email", email).order("time", desc=True).execute()
    return res.data

# -------------------------
# Meals Logging Endpoints
# -------------------------
class MealEntry(BaseModel):
    mealtype: Literal['breakfast', 'lunch', 'dinner', 'snacks']
    description: str
    calories: float
    proteins: float
    carbs: float
    fat: float

@router.post("/meals", response_model=dict)
def log_meal(data: MealEntry, email: str = Depends(get_user_email_from_token)):
    supabase.table("meals").insert({
        "email": email,
        "time": datetime.now().isoformat(),
        "mealtype": data.mealtype,
        "description": data.description,
        "calories": data.calories,
        "proteins": data.proteins,
        "carbs": data.carbs,
        "fat": data.fat,
    }).execute()
    return {"message": "Meal entry saved"}

@router.get("/meals", response_model=List[MealEntry])
def get_meal_logs(email: str = Depends(get_user_email_from_token)):
    res = supabase.table("meals").select("time, mealtype, description, calories, proteins, carbs, fat").eq("email", email).order("time", desc=True).execute()
    return res.data