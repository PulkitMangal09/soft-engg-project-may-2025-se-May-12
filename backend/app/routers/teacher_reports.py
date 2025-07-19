from fastapi import APIRouter, Path, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from typing import Any, Dict, List
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
        .select("grade_level")
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
    latest_alert = (
        supabase.table("health_alerts")
        .select("alert_type,title,description,triggered_at,severity")
        .eq("user_id", student_id)
        .eq("is_active", True)
        .order("triggered_at", desc=True)
        .limit(1)
        .execute()
        .data
    )
    alert_info = latest_alert[0] if latest_alert else None

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

    # 5) recent activity (mix task completions & health alerts)
    comps = supabase.table("task_completions")\
        .select("completed_at, notes")\
        .eq("student_id", student_id)\
        .order("completed_at", desc=True)\
        .limit(5)\
        .execute().data or []

    alerts = supabase.table("health_alerts")\
        .select("triggered_at, title")\
        .eq("user_id", student_id)\
        .order("triggered_at", desc=True)\
        .limit(5)\
        .execute().data or []

    # merge and sort
    events = []
    for c in comps:
        events.append({
            "when": c["completed_at"],
            "what": f"Completed task ({c.get('notes','')})"
        })
    for a in alerts:
        events.append({
            "when": a["triggered_at"],
            "what": a["title"]
        })
    events = sorted(events, key=lambda e: e["when"], reverse=True)[:5]

    return {
        "id": student_id,
        "full_name": user.get("full_name"),
        "email": user.get("email"),
        "grade_level": student.get("grade_level"),

        "healthSummary": {
            "conditions": conditions,
            "latestAlert": alert_info
        },

        "academicPerformance": {
            "totalTasks": total,
            "completedTasks": done,
            "completionRate": pct,
            "improvement": improvement
        },

        "recentActivity": events
    }
