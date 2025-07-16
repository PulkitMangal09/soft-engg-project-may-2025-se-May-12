from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
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
# Health Metrics
# -------------------------
class HealthMetricsRequest(BaseModel):
    weight: float
    height: float
    systolic: int
    diastolic: int
    blood_sugar: int
    heart_rate: int
    notes: Optional[str] = ""

class HealthMetricsResponse(BaseModel):
    weight: float
    height: float
    bmi: float
    systolic: int
    diastolic: int
    blood_sugar: int
    heart_rate: int
    notes: Optional[str]
    time: datetime

@router.post("/metrics", response_model=dict)
def add_health_metrics(
    data: HealthMetricsRequest,
    email: str = Depends(get_user_email_from_token)
):
    bmi = round(data.weight / ((data.height / 100) ** 2), 1)
    res = supabase.table("health_metrics").insert({
        "email": email,
        "weight": data.weight,
        "height": data.height,
        "systolic": data.systolic,
        "diastolic": data.diastolic,
        "blood_sugar": data.blood_sugar,
        "heart_rate": data.heart_rate,
        "bmi": bmi,
        "notes": data.notes,
        "created_at": datetime.now().isoformat()
    }).execute()
    return {"message": "Health metrics saved"}

@router.get("/metrics", response_model=HealthMetricsResponse)
def get_latest_metrics(email: str = Depends(get_user_email_from_token)):
    res = supabase.table("health_metrics").select("*").eq("email", email).order("created_at", desc=True).limit(1).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="No metrics found")
    m = res.data[0]
    return HealthMetricsResponse(
        weight=m['weight'],
        height=m['height'],
        bmi=m['bmi'],
        systolic=m['systolic'],
        diastolic=m['diastolic'],
        blood_sugar=m['blood_sugar'],
        heart_rate=m['heart_rate'],
        notes=m.get('notes'),
        time=m['created_at']
    )

# -------------------------
# Health Analytics
# -------------------------

class TrendPoint(BaseModel):
    time: datetime
    value: float

class TrendResponse(BaseModel):
    weight: List[TrendPoint]
    blood_sugar: List[TrendPoint]
    systolic: List[TrendPoint]
    diastolic: List[TrendPoint]
    heart_rate: List[TrendPoint]
    calories: float
    sugar: float
    sodium: float

@router.get("/analytics", response_model=TrendResponse)
def get_analytics(email: str = Depends(get_user_email_from_token)):
    metrics = supabase.table("health_metrics").select("created_at, weight, systolic, diastolic, blood_sugar, heart_rate").eq("email", email).order("created_at").execute()
    diet = supabase.table("student_diet").select("sugar, sodium, time").eq("email", email).execute()
    meals = supabase.table("meals").select("calories").eq("email", email).execute()

    return TrendResponse(
        weight=[{"time": m["created_at"], "value": m["weight"]} for m in metrics.data],
        blood_sugar=[{"time": m["created_at"], "value": m["blood_sugar"]} for m in metrics.data],
        systolic=[{"time": m["created_at"], "value": m["systolic"]} for m in metrics.data],
        diastolic=[{"time": m["created_at"], "value": m["diastolic"]} for m in metrics.data],
        heart_rate=[{"time": m["created_at"], "value": m["heart_rate"]} for m in metrics.data],
        sugar=sum(d.get("sugar", 0) for d in diet.data),
        sodium=sum(d.get("sodium", 0) for d in diet.data),
        calories=sum(m.get("calories", 0) for m in meals.data)
    )
