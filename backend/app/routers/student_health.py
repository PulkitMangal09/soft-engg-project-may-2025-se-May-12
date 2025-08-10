from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
from fastapi.security import OAuth2PasswordBearer
from ..config import supabase
from ..models import HealthMetricsRequest, HealthMetricsResponse, TrendPoint, TrendResponse
import jwt
from datetime import datetime
from uuid import UUID

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
@router.get("/metrics", response_model=HealthMetricsResponse)
def get_latest_metrics(email: str = Depends(get_user_email_from_token)):
    child_id = supabase.table("students").select("student_id").eq("email", email).execute()
    res = supabase.table("health_metrics").select("*").eq("student_id", child_id.data[0]['student_id']).order("created_at", desc=True).limit(1).execute()
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
        age_years=m.get('age_years'),
        sex=m.get('sex'),
        notes=m.get('notes'),
        time=m['created_at']
    )
@router.post("/metrics", response_model=dict)
def add_health_metrics(
    data: HealthMetricsRequest,
    email: str = Depends(get_user_email_from_token)
):
    bmi = round(data.weight / ((data.height / 100) ** 2), 1)
    child_id = supabase.table("students").select("student_id").eq("email", email).execute()
    # determine if sex already set for this student
    sex_check = (
        supabase.table("health_metrics")
        .select("sex")
        .eq("student_id", child_id.data[0]['student_id'])
        .neq("sex", None)
        .limit(1)
        .execute()
    )
    sex_locked = bool(sex_check.data)

    payload = {
        "student_id": child_id.data[0]['student_id'],
        "weight": data.weight,
        "height": data.height,
        "systolic": data.systolic,
        "diastolic": data.diastolic,
        "blood_sugar": data.blood_sugar,
        "heart_rate": data.heart_rate,
        "bmi": bmi,
        "age_years": data.age_years,
        "notes": data.notes,
        "created_at": datetime.now().isoformat()
    }
    if not sex_locked and getattr(data, 'sex', None):
        payload["sex"] = data.sex
    res = supabase.table("health_metrics").insert(payload).execute()
    return {"message": "Health metrics saved"}

@router.patch("/metrics/{entry_id}", response_model=dict)
def update_health_metrics(
    entry_id: UUID,
    data: HealthMetricsRequest,
    email: str = Depends(get_user_email_from_token)
):
    bmi = round(data.weight / ((data.height / 100) ** 2), 1)
    child_id = supabase.table("students").select("student_id").eq("email", email).execute()
    
    # check if sex already set; if yes, ignore incoming sex updates
    sex_check = (
        supabase.table("health_metrics")
        .select("sex")
        .eq("student_id", child_id.data[0]['student_id'])
        .neq("sex", None)
        .limit(1)
        .execute()
    )
    sex_locked = bool(sex_check.data)

    update_payload = {
        "weight": data.weight,
        "height": data.height,
        "systolic": data.systolic,
        "diastolic": data.diastolic,
        "blood_sugar": data.blood_sugar,
        "heart_rate": data.heart_rate,
        "bmi": bmi,
        "age_years": data.age_years,
        "notes": data.notes,
    }
    if not sex_locked and getattr(data, 'sex', None):
        update_payload["sex"] = data.sex
    result = (
        supabase.table("health_metrics")
        .update(update_payload)
        .eq("id", str(entry_id))
        .eq("student_id", child_id.data[0]['student_id'])
        .execute()
    )

    if not result.data:
        raise HTTPException(status_code=404, detail="Metric entry not found or unauthorized")

    return {"message": "Health metric updated"}

# DELETE: Remove a specific health metric entry
@router.delete("/metrics/{entry_id}", response_model=dict)
def delete_health_metrics(
    entry_id: UUID,
    email: str = Depends(get_user_email_from_token)
):
    child_id = supabase.table("students").select("student_id").eq("email", email).execute()

    result = supabase.table("health_metrics").delete().eq("id", str(entry_id)).eq("student_id", child_id.data[0]['student_id']).execute()

    if not result.data:
        raise HTTPException(status_code=404, detail="Metric entry not found or unauthorized")

    return {"message": "Health metric deleted"}


# -------------------------
# Health Analytics
# -------------------------



@router.get("/analytics", response_model=TrendResponse)
def get_analytics(email: str = Depends(get_user_email_from_token)):
    child_id = supabase.table("students").select("student_id").eq("email", email).execute()
    metrics = supabase.table("health_metrics").select("created_at, weight, systolic, diastolic, blood_sugar, heart_rate").eq("student_id", child_id.data[0]['student_id']).order("created_at").execute()
    diet = supabase.table("student_diet").select("sugar, sodium, time").eq("student_id", child_id.data[0]['student_id']).execute()
    meals = supabase.table("meals").select("calories").eq("student_id", child_id.data[0]['student_id']).execute()

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
