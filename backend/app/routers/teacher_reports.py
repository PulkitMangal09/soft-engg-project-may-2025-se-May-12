from fastapi import APIRouter, Path, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from typing import Any, Dict, List, Optional
from fastapi import Query
from datetime import date, timedelta
from ..config import supabase

router = APIRouter(prefix="/teacher/reports", tags=["teacher-reports"])
oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/token")


def get_teacher_id(token: str) -> str:
    auth = supabase.auth.get_user(token)
    if getattr(auth, "error", None):
        raise HTTPException(status_code=401, detail="Unauthorized")
    # confirm they exist in teachers table
    t = (
        supabase.table("teachers")
        .select("teacher_id")
        .eq("teacher_id", auth.user.id)
        .single()
        .execute()
        .data
    )
    if not t:
        raise HTTPException(status_code=403, detail="Forbidden")
    return auth.user.id


@router.get("/students", response_model=List[Dict[str, Any]])
def list_students(token: str = Depends(oauth2)):
    """Return students assigned to the authenticated teacher with basic fields.
    """
    teacher_id = get_teacher_id(token)

    # Find classrooms for this teacher
    classes = (
        supabase.table("classrooms")
        .select("classroom_id")
        .eq("teacher_id", teacher_id)
        .execute()
        .data
        or []
    )
    if not classes:
        return []

    classroom_ids = [c["classroom_id"] for c in classes if c.get("classroom_id")]
    if not classroom_ids:
        return []

    # Get active enrollments for those classrooms
    enrollments = (
        supabase.table("classroom_students")
        .select("student_id")
        .in_("classroom_id", classroom_ids)
        .eq("is_active", True)
        .execute()
        .data
        or []
    )
    student_ids = sorted({e.get("student_id") for e in enrollments if e.get("student_id")})
    if not student_ids:
        return []

    # Fetch student rows for grade_level and optional fields
    stu_resp = (
        supabase.table("students")
        .select("student_id, student_number, grade_level, email, name")
        .in_("student_id", student_ids)
        .execute()
    )
    students = {s["student_id"]: s for s in (getattr(stu_resp, "data", None) or [])}

    # Fetch profile info from users (note: schema has no avatar_url)
    users_resp = (
        supabase.table("users")
        .select("user_id, full_name, email")
        .in_("user_id", student_ids)
        .execute()
    )
    users = {u["user_id"]: u for u in (getattr(users_resp, "data", None) or [])}

    out: List[Dict[str, Any]] = []
    for sid in student_ids:
        s = students.get(sid, {})
        u = users.get(sid, {})
        out.append({
            "student_id": sid,
            "student_number": s.get("student_number"),
            "full_name": u.get("full_name") or s.get("name"),
            "email": u.get("email") or s.get("email"),
            "grade_level": s.get("grade_level"),
        })
    return out


@router.get("/{student_id}", response_model=Dict[str, Any])
def student_report(
    student_id: str = Path(..., description="The UUID of the student"),
    token: str = Depends(oauth2),
):
    teacher_id = get_teacher_id(token)

    # 1) ensure this student is in one of their classrooms
    classes = (
        supabase.table("classrooms")
        .select("classroom_id")
        .eq("teacher_id", teacher_id)
        .execute()
        .data
        or []
    )
    if not classes:
        raise HTTPException(404, "No classrooms found for teacher")

    classroom_ids = [c["classroom_id"] for c in classes]
    membership = (
        supabase.table("classroom_students")
        .select("*")
        .in_("classroom_id", classroom_ids)
        .eq("student_id", student_id)
        .single()
        .execute()
        .data
    )
    if not membership:
        raise HTTPException(404, "Student not found in your classes")

    # 2) basic profile
    user = (
        supabase.table("users")
        .select("full_name,email")
        .eq("user_id", student_id)
        .single()
        .execute()
        .data
        or {}
    )
    student = (
        supabase.table("students")
        .select("grade_level, student_number, emergency_contact_phone")
        .eq("student_id", student_id)
        .single()
        .execute()
        .data
        or {}
    )

    # 3) health summary
    conditions = (
        supabase.table("health_conditions")
        .select("condition_name,severity")
        .eq("user_id", student_id)
        .eq("is_active", True)
        .execute()
        .data
        or []
    )
    # latest nutrition suggestions (replace non-existent health_alerts)
    latest_nutri = (
        supabase.table("nutrition_suggestions")
        .select("generated_at, range_key, suggestions")
        .eq("user_id", student_id)
        .order("generated_at", desc=True)
        .limit(1)
        .execute()
        .data
    )
    nutri_info = None
    if latest_nutri:
        n = latest_nutri[0]
        # send a compact summary (count) to avoid large payloads
        try:
            sugg = n.get("suggestions") or []
            count = len(sugg) if isinstance(sugg, list) else 1
        except Exception:
            count = None
        nutri_info = {
            "generated_at": n.get("generated_at"),
            "range_key": n.get("range_key"),
            "count": count,
        }

    # 4) academic performance
    # tasks *assigned_by* this teacher to this student
    tasks = (
        supabase.table("tasks")
        .select("status")
        .eq("assigned_to", student_id)
        .eq("assigned_by", teacher_id)
        .execute()
        .data
        or []
    )
    total = len(tasks)
    done = len([t for t in tasks if t["status"] == "completed"])
    pct = f"{(done/total*100):.0f}%" if total else "N/A"

    # simple “improvement trend” from comparing this month vs last
    today = date.today()
    start_of_month = today.replace(day=1)
    last_month_start = (start_of_month - timedelta(days=1)).replace(day=1)

    this_month_done = len(
        supabase.table("tasks")
        .select("status")
        .eq("assigned_to", student_id)
        .eq("assigned_by", teacher_id)
        .eq("status", "completed")
        .gte("completion_date", start_of_month.isoformat())
        .execute()
        .data
        or []
    )
    last_month_done = len(
        supabase.table("tasks")
        .select("status")
        .eq("assigned_to", student_id)
        .eq("assigned_by", teacher_id)
        .eq("status", "completed")
        .gte("completion_date", last_month_start.isoformat())
        .lt("completion_date", start_of_month.isoformat())
        .execute()
        .data
        or []
    )
    improvement = None
    if last_month_done:
        improvement = f"{((this_month_done/last_month_done - 1)*100):+.0f}%"
    elif this_month_done:
        improvement = "+100%"

    # 5) recent activity (mix task assignments, task completions & nutrition suggestions)
    # Recent task assignments (by this teacher to this student)
    assigned = supabase.table("tasks")\
        .select("title, created_at")\
        .eq("assigned_to", student_id)\
        .eq("assigned_by", teacher_id)\
        .order("created_at", desc=True)\
        .limit(5)\
        .execute().data or []

    # Recent task completions
    comps = supabase.table("task_completions")\
        .select("completed_at, notes")\
        .eq("student_id", student_id)\
        .order("completed_at", desc=True)\
        .limit(5)\
        .execute().data or []
    # Nutrition suggestions as events
    nutri_recent = supabase.table("nutrition_suggestions")\
        .select("generated_at, range_key")\
        .eq("user_id", student_id)\
        .order("generated_at", desc=True)\
        .limit(5)\
        .execute().data or []

    # merge and sort
    events = []
    for t in assigned:
        events.append({
            "when": t.get("created_at"),
            "what": f"Task assigned ({t.get('title', '')})"
        })
    for c in comps:
        events.append({
            "when": c["completed_at"],
            "what": f"Completed task ({c.get('notes','')})"
        })
    for n in nutri_recent:
        events.append({
            "when": n["generated_at"],
            "what": f"Nutrition suggestions generated ({n.get('range_key','')})"
        })
    events = sorted(events, key=lambda e: e["when"], reverse=True)[:5]

    return {
        "id": student_id,
        "full_name": user.get("full_name"),
        "email": user.get("email"),
        "student_number": student.get("student_number"),
        "grade_level": student.get("grade_level"),
        "emergency_contact_phone": student.get("emergency_contact_phone"),

        "healthSummary": {
            "conditions": conditions,
            "latestNutrition": nutri_info
        },

        "academicPerformance": {
            "totalTasks": total,
            "completedTasks": done,
            "completionRate": pct,
            "improvement": improvement
        },

        "recentActivity": events
    }


@router.get("/{student_id}/nutrition_suggestions", response_model=List[Dict[str, Any]])
def list_nutrition_suggestions(
    student_id: str = Path(..., description="The UUID of the student"),
    limit: int = Query(5, ge=1, le=50),
    generated_at: Optional[str] = Query(None, description="If provided, return the suggestion with this generated_at"),
    token: str = Depends(oauth2),
):
    """Return nutrition suggestions for a student the teacher has in their classes.

    - If generated_at is provided, returns at most one matching record.
    - Otherwise, returns up to `limit` recent suggestions.
    """
    teacher_id = get_teacher_id(token)

    # ensure relationship via classroom membership
    classes = (
        supabase.table("classrooms").select("classroom_id").eq("teacher_id", teacher_id).execute().data or []
    )
    if not classes:
        raise HTTPException(404, "No classrooms found for teacher")
    classroom_ids = [c["classroom_id"] for c in classes]
    membership = (
        supabase.table("classroom_students")
        .select("student_id")
        .in_("classroom_id", classroom_ids)
        .eq("student_id", student_id)
        .single()
        .execute()
        .data
    )
    if not membership:
        raise HTTPException(404, "Student not found in your classes")

    qry = supabase.table("nutrition_suggestions").select("*").eq("user_id", student_id)
    if generated_at:
        # exact match on timestamp string produced by API; client can pass value from events/latestNutrition
        res = qry.eq("generated_at", generated_at).order("generated_at", desc=True).limit(1).execute()
        return res.data or []
    else:
        res = qry.order("generated_at", desc=True).limit(limit).execute()
        return res.data or []
