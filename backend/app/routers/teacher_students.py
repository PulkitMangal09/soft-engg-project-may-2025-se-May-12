# app/routers/teacher_students.py
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import List, Dict, Any
from uuid import UUID
from pydantic import BaseModel
from ..config import supabase

router = APIRouter(prefix="/teacher", tags=["teacher-students"])
oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/token")

class ClassroomCreate(BaseModel):
    name: str
    subject: str
    description: str = ""
    grade_level: str = ""

def get_teacher_id(token: str) -> UUID:
    auth = supabase.auth.get_user(token)
    if getattr(auth, "error", None):
        raise HTTPException(401, "Unauthorized")
    # verify they are actually a teacher
    teacher = (
        supabase.table("teachers")
        .select("teacher_id")
        .eq("teacher_id", auth.user.id)
        .single()
        .execute()
        .data
    )
    if not teacher:
        raise HTTPException(403, "Forbidden")
    return auth.user.id

@router.get("/classrooms", response_model=List[Dict[str, Any]])
def list_classrooms(token: str = Depends(oauth2)):
    """List all classrooms owned by this teacher."""
    teacher_id = get_teacher_id(token)
    resp = (
        supabase.table("classrooms")
        .select("*")
        .eq("teacher_id", teacher_id)
        .execute()
    )
    return resp.data or []

@router.post("/classrooms", response_model=Dict[str, Any])
def create_classroom(classroom: ClassroomCreate, token: str = Depends(oauth2)):
    """Create a new classroom for this teacher."""
    teacher_id = get_teacher_id(token)
    
    # Insert new classroom
    resp = (
        supabase.table("classrooms")
        .insert({
            "name": classroom.name,
            "subject": classroom.subject,
            "description": classroom.description,
            "grade_level": classroom.grade_level,
            "teacher_id": teacher_id,
        })
        .execute()
    )
    
    if not resp.data:
        raise HTTPException(400, "Failed to create classroom")
    
    return resp.data[0]

@router.get("/classrooms/{classroom_id}/students", response_model=List[Dict[str, Any]])
def list_classroom_students(classroom_id: UUID, token: str = Depends(oauth2)):
    """List all students in a given classroom."""
    teacher_id = get_teacher_id(token)
    # confirm classroom belongs to teacher
    cls = (
        supabase.table("classrooms")
        .select("classroom_id")
        .eq("classroom_id", classroom_id)
        .eq("teacher_id", teacher_id)
        .single()
        .execute()
        .data
    )
    if not cls:
        raise HTTPException(404, "Classroom not found")
    # join through classroom_students → fetch student profiles
    join = (
        supabase.table("classroom_students")
        .select("student_id, students ( user_id, full_name, grade_level )")
        .eq("classroom_id", classroom_id)
        .execute()
    )
    return [
        {
          "student_id": r["student_id"],
          **r["students"]
        }
        for r in join.data or []
    ]

@router.post("/classrooms/{classroom_id}/students/{student_id}", response_model=dict)
def add_student_to_class(classroom_id: UUID, student_id: UUID, token: str = Depends(oauth2)):
    """Enroll a student into a classroom."""
    teacher_id = get_teacher_id(token)
    # ensure teacher owns this classroom
    cls = (
        supabase.table("classrooms")
        .select("classroom_id")
        .eq("classroom_id", classroom_id)
        .eq("teacher_id", teacher_id)
        .single()
        .execute()
        .data
    )
    if not cls:
        raise HTTPException(404, "Classroom not found")
    # insert join
    supabase.table("classroom_students").insert({
        "classroom_id": classroom_id,
        "student_id": student_id
    }).execute()
    return {"added": True}

@router.delete("/classrooms/{classroom_id}/students/{student_id}", response_model=dict)
def remove_student_from_class(classroom_id: UUID, student_id: UUID, token: str = Depends(oauth2)):
    """Remove a student from a classroom."""
    teacher_id = get_teacher_id(token)
    # same ownership guard
    cls = (
        supabase.table("classrooms")
        .select("classroom_id")
        .eq("classroom_id", classroom_id)
        .eq("teacher_id", teacher_id)
        .single()
        .execute()
        .data
    )
    if not cls:
        raise HTTPException(404, "Classroom not found")
    supabase.table("classroom_students")\
        .delete()\
        .eq("classroom_id", classroom_id)\
        .eq("student_id", student_id)\
        .execute()
    return {"removed": True}

# Optional: aggregate simple “need help / health alerts / top performers” metrics
@router.get("/students/metrics", response_model=List[Dict[str, Any]])
def students_metrics(token: str = Depends(oauth2)):
    """
    Return for each student across all this teacher's classrooms:
      - total tasks assigned & completed
      - overdue count
      - health alert count
      - average grade (if you have a grades table)
    """
    teacher_id = get_teacher_id(token)

    # 1) find all student_ids in their classrooms
    students = supabase.table("classroom_students")\
        .select("student_id")\
        .in_("classroom_id",
             [c["classroom_id"] for c in supabase.table("classrooms")
               .select("classroom_id")
               .eq("teacher_id", teacher_id)
               .execute().data or []
             ])\
        .execute().data or []

    out = []
    for s in students:
        sid = s["student_id"]
        # tasks summary
        t = supabase.rpc("teacher_student_task_summary", {   # you can create an RPC for this
            "teacher_id": teacher_id,
            "student_id": sid
        }).execute().data or {}
        # health alerts
        alerts = supabase.table("health_alerts")\
          .select("alert_id")\
          .eq("user_id", sid)\
          .eq("is_active", True)\
          .execute().data or []
        out.append({
          "student_id": sid,
          "tasks_assigned": t.get("assigned", 0),
          "tasks_completed": t.get("completed", 0),
          "tasks_overdue": t.get("overdue", 0),
          "health_alerts": len(alerts),
          # "average_grade": ...
        })
    return out
