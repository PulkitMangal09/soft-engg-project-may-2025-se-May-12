from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi.security import OAuth2PasswordBearer
from typing import Any, Dict, List, Optional
from datetime import date, datetime, timedelta
from uuid import UUID

from ..config import supabase

router = APIRouter(prefix="/parent/reports", tags=["parent-reports"])
oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/token")


# -------------------------
# Helpers: family-based auth
# -------------------------

def _get_parent_children_ids(parent_user_id: str) -> List[str]:
    """Return active child user_ids for families where user is head/parent."""
    head_resp = (
        supabase.table("family_groups")
        .select("family_id")
        .eq("family_head_id", str(parent_user_id))
        .eq("is_active", True)
        .execute()
    )
    head_family_ids = {row.get("family_id") for row in (getattr(head_resp, "data", None) or [])}

    member_resp = (
        supabase.table("family_members")
        .select("family_id, role, is_active")
        .eq("user_id", str(parent_user_id))
        .eq("is_active", True)
        .execute()
    )
    member_family_ids = {
        row.get("family_id")
        for row in (getattr(member_resp, "data", None) or [])
        if row.get("role") in ("head", "parent")
    }
    family_ids = list(head_family_ids.union(member_family_ids))
    if not family_ids:
        return []

    fm_resp = (
        supabase.table("family_members")
        .select("user_id, role, is_active")
        .in_("family_id", family_ids)
        .eq("role", "child")
        .eq("is_active", True)
        .execute()
    )
    child_ids: List[str] = []
    for row in (getattr(fm_resp, "data", None) or []):
        uid = row.get("user_id")
        if uid:
            child_ids.append(uid)
    return child_ids


def _require_parent_and_children(token: str) -> tuple[str, List[str]]:
    auth = supabase.auth.get_user(token)
    user = getattr(auth, "user", None)
    if not user or not user.id:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    children = _get_parent_children_ids(user.id)
    return user.id, children


# -------------------------
# Endpoints
# -------------------------

@router.get("/students", response_model=List[Dict[str, Any]])
def list_student_children(token: str = Depends(oauth2)):
    parent_id, child_ids = _require_parent_and_children(token)
    if not child_ids:
        return []

    # users info
    users_resp = (
        supabase.table("users").select("user_id, full_name, email").in_("user_id", child_ids).execute()
    )
    users = {u["user_id"]: u for u in (getattr(users_resp, "data", None) or [])}

    # students info (grade)
    st_resp = (
        supabase.table("students").select("student_id, grade_level").in_("student_id", child_ids).execute()
    )
    students = {s["student_id"]: s for s in (getattr(st_resp, "data", None) or [])}

    out: List[Dict[str, Any]] = []
    for sid in child_ids:
        u = users.get(sid, {})
        s = students.get(sid, {})
        out.append({
            "student_id": sid,
            "full_name": u.get("full_name"),
            "email": u.get("email"),
            "grade_level": s.get("grade_level"),
        })
    return out


@router.get("/{student_id}", response_model=Dict[str, Any])
def get_student_report(student_id: str = Path(...), token: str = Depends(oauth2)):
    parent_id, child_ids = _require_parent_and_children(token)
    if student_id not in child_ids:
        raise HTTPException(status_code=403, detail="You are not authorized to view this student")

    # Basic profile
    user_row = (
        supabase.table("users").select("full_name, email").eq("user_id", student_id).single().execute().data or {}
    )
    stud_row = (
        supabase.table("students").select("grade_level, student_number").eq("student_id", student_id).single().execute().data or {}
    )

    # Medical conditions (active)
    conditions = (
        supabase.table("health_conditions")
        .select("condition_id, condition_name, severity, diagnosed_date, dietary_restrictions, is_active")
        .eq("user_id", student_id)
        .eq("is_active", True)
        .order("created_at", desc=True)
        .execute()
        .data
        or []
    )

    # Medications (all) and logs (last 7d)
    meds = (
        supabase.table("medications")
        .select("medication_id, medication_name, dosage, frequency, start_date, end_date")
        .eq("user_id", student_id)
        .order("created_at", desc=True)
        .execute()
        .data
        or []
    )
    start_dt = (datetime.now() - timedelta(days=7)).isoformat()
    end_dt = datetime.now().isoformat()
    med_logs = (
        supabase.table("medication_logs")
        .select("log_id, medication_id, taken_at, quantity_taken, notes")
        .eq("user_id", student_id)
        .gte("taken_at", start_dt)
        .lt("taken_at", end_dt)
        .order("taken_at", desc=True)
        .execute()
        .data
        or []
    )

    # Water intake (today)
    today = date.today().isoformat()
    water_logs = (
        supabase.table("water_intake")
        .select("intake_id, amount_ml, container_type, intake_time, intake_date")
        .eq("user_id", student_id)
        .eq("intake_date", today)
        .order("intake_time")
        .execute()
        .data
        or []
    )
    total_ml = sum(int(w.get("amount_ml") or 0) for w in water_logs)

    # Meals (today)
    start_today = f"{today} 00:00:00"
    end_today = f"{(date.today() + timedelta(days=1)).isoformat()} 00:00:00"
    meals = (
        supabase.table("meals")
        .select("id, time, mealtype, description, calories, sodium, sugar")
        .eq("student_id", student_id)
        .gte("time", start_today)
        .lt("time", end_today)
        .order("time", desc=True)
        .execute()
        .data
        or []
    )

    # Latest health metrics
    metrics = (
        supabase.table("health_metrics")
        .select("created_at, weight, height, bmi, systolic, diastolic, blood_sugar, heart_rate, notes, age_years, sex")
        .eq("student_id", student_id)
        .order("created_at", desc=True)
        .limit(1)
        .execute()
        .data
    )
    latest_metrics = (metrics or [None])[0]

    # Latest nutrition suggestions
    latest_sugg = (
        supabase.table("nutrition_suggestions")
        .select("generated_at, range_key, suggestions")
        .eq("user_id", student_id)
        .order("generated_at", desc=True)
        .limit(1)
        .execute()
        .data
    )
    latest_nutrition = (latest_sugg or [None])[0]

    # Return aggregated
    return {
        "id": student_id,
        "profile": {
            "full_name": user_row.get("full_name"),
            "email": user_row.get("email"),
            "grade_level": stud_row.get("grade_level"),
            "student_number": stud_row.get("student_number"),
        },
        "medical": {
            "conditions": conditions,
            "medications": meds,
            "medication_logs": med_logs,
        },
        "water": {
            "today_total_ml": total_ml,
            "logs": water_logs,
        },
        "meals": meals,
        "health_metrics_latest": latest_metrics,
        "nutrition_suggestion_latest": latest_nutrition,
    }
