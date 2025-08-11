from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from typing import List, Optional
from uuid import UUID
from datetime import datetime, timezone, timedelta

from ..config import supabase
from ..models import (
    HealthConditionCreate, HealthConditionUpdate, HealthConditionOut,
    MedicationCreate, MedicationUpdate, MedicationOut,
    MedicationLogCreate, MedicationLogOut
)
import jwt

router = APIRouter(prefix="/medical", tags=["medical"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

# Timezone helpers
IST_TZ = timezone(timedelta(hours=5, minutes=30))

def to_ist_iso(dt: datetime | None) -> str:
    """Return ISO string in IST. If dt is naive, assume UTC then convert to IST.
    If dt is None, use current time in IST.
    """
    if dt is None:
        return datetime.now(tz=IST_TZ).isoformat()
    if dt.tzinfo is None:
        # assume incoming naive times are UTC
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(IST_TZ).isoformat()


def get_user_email_from_token(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = jwt.decode(token, options={"verify_signature": False})
        email = payload.get("email")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        return email
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


def get_student_id(email: str) -> UUID:
    res = supabase.table("students").select("student_id").eq("email", email).limit(1).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Student not found")
    return res.data[0]["student_id"]


# -------------------------
# Conditions
# -------------------------
@router.get("/conditions", response_model=List[HealthConditionOut])
def list_conditions(email: str = Depends(get_user_email_from_token)):
    student_id = get_student_id(email)
    res = supabase.table("health_conditions").select("*").eq("user_id", student_id).order("created_at", desc=True).execute()
    return res.data or []


@router.post("/conditions", response_model=HealthConditionOut)
def create_condition(payload: HealthConditionCreate, email: str = Depends(get_user_email_from_token)):
    student_id = get_student_id(email)
    insert_data = {
        "user_id": student_id,
        "condition_name": payload.condition_name,
        "severity": payload.severity,
        "diagnosed_date": payload.diagnosed_date.isoformat() if payload.diagnosed_date else None,
        "doctor_clinic": payload.doctor_clinic,
        "dietary_restrictions": payload.dietary_restrictions,
        "symptoms_to_monitor": payload.symptoms_to_monitor,
        "is_active": payload.is_active,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
    }
    res = supabase.table("health_conditions").insert(insert_data).execute()
    return res.data[0]


@router.patch("/conditions/{condition_id}", response_model=dict)
def update_condition(condition_id: UUID, payload: HealthConditionUpdate, email: str = Depends(get_user_email_from_token)):
    student_id = get_student_id(email)
    update_data = {k: v for k, v in payload.model_dump(exclude_unset=True).items()}
    if "diagnosed_date" in update_data and update_data["diagnosed_date"]:
        update_data["diagnosed_date"] = update_data["diagnosed_date"].isoformat()
    update_data["updated_at"] = datetime.now().isoformat()
    res = supabase.table("health_conditions").update(update_data).eq("condition_id", str(condition_id)).eq("user_id", student_id).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Condition not found or unauthorized")
    return {"message": "Condition updated"}


@router.delete("/conditions/{condition_id}", response_model=dict)
def delete_condition(condition_id: UUID, email: str = Depends(get_user_email_from_token)):
    student_id = get_student_id(email)
    res = supabase.table("health_conditions").delete().eq("condition_id", str(condition_id)).eq("user_id", student_id).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Condition not found or unauthorized")
    return {"message": "Condition deleted"}


# -------------------------
# Medications
# -------------------------
@router.get("/medications", response_model=List[MedicationOut])
def list_medications(condition_id: Optional[UUID] = None, email: str = Depends(get_user_email_from_token)):
    student_id = get_student_id(email)
    query = supabase.table("medications").select("*").eq("user_id", student_id)
    if condition_id:
        query = query.eq("condition_id", str(condition_id))
    res = query.order("created_at", desc=True).execute()
    return res.data or []


@router.post("/medications", response_model=MedicationOut)
def create_medication(payload: MedicationCreate, email: str = Depends(get_user_email_from_token)):
    student_id = get_student_id(email)
    insert_data = payload.model_dump()
    insert_data.update({
        "user_id": student_id,
        "condition_id": str(payload.condition_id) if payload.condition_id else None,
        "start_date": payload.start_date.isoformat() if payload.start_date else None,
        "end_date": payload.end_date.isoformat() if payload.end_date else None,
        "created_at": datetime.now().isoformat(),
    })
    res = supabase.table("medications").insert(insert_data).execute()
    return res.data[0]


@router.patch("/medications/{medication_id}", response_model=dict)
def update_medication(medication_id: UUID, payload: MedicationUpdate, email: str = Depends(get_user_email_from_token)):
    student_id = get_student_id(email)
    update_data = {k: v for k, v in payload.model_dump(exclude_unset=True).items()}
    if "condition_id" in update_data and update_data["condition_id"]:
        update_data["condition_id"] = str(update_data["condition_id"])
    if "start_date" in update_data and update_data["start_date"]:
        update_data["start_date"] = update_data["start_date"].isoformat()
    if "end_date" in update_data and update_data["end_date"]:
        update_data["end_date"] = update_data["end_date"].isoformat()
    res = supabase.table("medications").update(update_data).eq("medication_id", str(medication_id)).eq("user_id", student_id).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Medication not found or unauthorized")
    return {"message": "Medication updated"}


@router.delete("/medications/{medication_id}", response_model=dict)
def delete_medication(medication_id: UUID, email: str = Depends(get_user_email_from_token)):
    student_id = get_student_id(email)
    res = supabase.table("medications").delete().eq("medication_id", str(medication_id)).eq("user_id", student_id).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Medication not found or unauthorized")
    return {"message": "Medication deleted"}


# -------------------------
# Medication Logs
# -------------------------
@router.get("/medications/{medication_id}/logs", response_model=List[MedicationLogOut])
def list_medication_logs(medication_id: UUID, email: str = Depends(get_user_email_from_token)):
    student_id = get_student_id(email)
    # ensure med belongs to student
    med = supabase.table("medications").select("medication_id").eq("medication_id", str(medication_id)).eq("user_id", student_id).limit(1).execute()
    if not med.data:
        raise HTTPException(status_code=404, detail="Medication not found or unauthorized")
    res = supabase.table("medication_logs").select("*").eq("medication_id", str(medication_id)).eq("user_id", student_id).order("taken_at", desc=True).execute()
    return res.data or []


@router.post("/medications/{medication_id}/logs", response_model=MedicationLogOut)
def create_medication_log(medication_id: UUID, payload: MedicationLogCreate, email: str = Depends(get_user_email_from_token)):
    student_id = get_student_id(email)
    # ensure med belongs to student
    med = supabase.table("medications").select("medication_id").eq("medication_id", str(medication_id)).eq("user_id", student_id).limit(1).execute()
    if not med.data:
        raise HTTPException(status_code=404, detail="Medication not found or unauthorized")
    # Normalize quantity_taken: if it's an integer-only input, append ' pill'
    normalized_quantity = payload.quantity_taken
    if normalized_quantity is not None:
        # If numeric type int => append unit
        if isinstance(normalized_quantity, int):
            normalized_quantity = f"{normalized_quantity} pill"
        else:
            # If string consisting of only digits (e.g., '1', '2') after trimming
            try:
                s = str(normalized_quantity).strip()
                if s.isdigit():
                    normalized_quantity = f"{s} pill"
            except Exception:
                # Fallback: keep original if any conversion issue
                pass
    insert_data = {
        "medication_id": str(medication_id),
        "user_id": student_id,
        "taken_at": to_ist_iso(payload.taken_at),
        "quantity_taken": normalized_quantity,
        "notes": payload.notes,
        "logged_by": student_id,
    }
    res = supabase.table("medication_logs").insert(insert_data).execute()
    return res.data[0]
