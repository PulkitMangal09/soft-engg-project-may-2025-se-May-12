# routers/parent.py
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.security import OAuth2PasswordBearer
from typing import List, Optional
from pydantic import BaseModel
from uuid import UUID
from ..config import supabase
from fastapi.responses import JSONResponse
import jwt

router = APIRouter(prefix="/parent", tags=["parent"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

# Extract parent email from token
def get_email_from_token(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = jwt.decode(token, options={"verify_signature": False})
        return payload.get("email")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

# Extract user_id from token
def get_user_id_from_token(token: str = Depends(oauth2_scheme)) -> UUID:
    try:
        payload = jwt.decode(token, options={"verify_signature": False})
        user_res = supabase.table("users").select("user_id").eq("email", payload.get("email")).single().execute()
        if not user_res.data:
            raise HTTPException(status_code=404, detail="User not found")
        user_id = user_res.data['user_id']
        return user_id
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

# -------------------------
# Part 1: View Child Metrics
# -------------------------
class ChildHealthSnapshot(BaseModel):
    full_name: str
    email: str
    weight: float
    height: float
    bmi: float
    systolic: int
    diastolic: int
    blood_sugar: int
    heart_rate: int
    notes: str
    created_at: str

@router.get("/children/metrics", response_model=List[ChildHealthSnapshot])
def view_all_children_metrics(parent_email: str = Depends(get_email_from_token)):
    user_res = supabase.table("users").select("user_id").eq("email", parent_email).single().execute()
    if not user_res.data:
        raise HTTPException(status_code=404, detail="User not found")
    user_id = user_res.data['user_id']

    parent = supabase.table("parents").select("parent_id").eq("user_id", user_id).single().execute()
    if not parent.data:
        raise HTTPException(status_code=404, detail="Parent not found")
    parent_id = parent.data['parent_id']

    link_res = supabase.table("parent_children").select("child_id").eq("parent_id", parent_id).execute()
    if not link_res.data:
        return []
    child_ids = [c['child_id'] for c in link_res.data]

    snapshots = []
    for child_id in child_ids:
        user_res = supabase.table("students").select("name, email").eq("student_id", child_id).single().execute()
        if not user_res.data:
            continue
        name = user_res.data['name']
        email = user_res.data['email']
        metric_res = supabase.table("health_metrics").select("*").eq("email", email).order("created_at", desc=True).limit(1).execute()
        if not metric_res.data:
            continue
        m = metric_res.data[0]
        snapshots.append(ChildHealthSnapshot(
            full_name=name,
            email=email,
            weight=m['weight'],
            height=m['height'],
            bmi=m['bmi'],
            systolic=m['systolic'],
            diastolic=m['diastolic'],
            blood_sugar=m['blood_sugar'],
            heart_rate=m['heart_rate'],
            notes=m.get('notes', ''),
            created_at=m['created_at']
        ))
    return snapshots

# -------------------------
# Part 2: Child Linking
# -------------------------
class ChildLinkRequest(BaseModel):
    child_id: UUID
    relationship: str

@router.get("/children")
def get_children(user_id: UUID = Depends(get_user_id_from_token)):
    parent = supabase.table("parents").select("parent_id").eq("user_id", user_id).single().execute()
    if not parent.data:
        raise HTTPException(status_code=404, detail="Parent not found")
    parent_id = parent.data['parent_id']

    children_ids = supabase.table("parent_children").select("child_id").eq("parent_id", parent_id).execute()
    child_ids = [c['child_id'] for c in children_ids.data]
    user_res=[]
    for child_id in child_ids:
        user_res.append(supabase.table("students").select("name, email, student_number, grade_level, school_name, student_id").eq("student_id", child_id).execute().data)
    return user_res

@router.post("/children/add")
def add_child(data: ChildLinkRequest, user_id: UUID = Depends(get_user_id_from_token)):
    child = supabase.table("students").select("student_id").eq("student_id", data.child_id).single().execute()
    if not child.data:
        raise HTTPException(status_code=404, detail="Child not found")

    parent = supabase.table("parents").select("parent_id").eq("user_id", user_id).single().execute()
    if not parent.data:
        raise HTTPException(status_code=404, detail="Parent not found")
    parent_id = parent.data['parent_id']

    supabase.table("parent_children").insert({
        "parent_id": str(parent_id),
        "child_id": str(data.child_id),
        "relationship": data.relationship
    }).execute()
    return {"message": "Child linked successfully"}

@router.delete("/children/remove")
def remove_child(child_id: UUID, user_id: UUID = Depends(get_user_id_from_token)):
    parent = supabase.table("parents").select("parent_id").eq("user_id", user_id).single().execute()
    if not parent.data:
        raise HTTPException(status_code=404, detail="Parent not found")
    parent_id = parent.data['parent_id']

    supabase.table("parent_children").delete().eq("parent_id", parent_id).eq("child_id", child_id).execute()
    return {"message": "Child unlinked successfully"}

@router.get("/children/search")
def search_child(email: Optional[str] = None, student_id: Optional[UUID] = None, name: Optional[str] = None, school_name: Optional[str] = None, grade_level: Optional[str] = None):
    query = supabase.table("students").select("student_id, email, name")
    if email:
        query = query.ilike("email", f"%{email}%")
    if student_id:
        query = query.eq("student_id", str(student_id))
    if name:
        query = query.ilike("name", f"%{name}%")
    if school_name:
        query = query.ilike("school_name", f"%{school_name}%")
    if grade_level:
        query = query.ilike("grade_level", f"%{grade_level}%")

    if not any([email, student_id, name, school_name, grade_level]):
        raise HTTPException(status_code=400, detail="Provide at least one search parameter")
    res = query.execute()
    return res.data

# -------------------------
# Part 3: Other Parents and Child Data
# -------------------------
class ParentDetails(BaseModel):
    parent_id: UUID
    name: str
    is_head: bool
    group: Optional[str]
    description: Optional[str]

@router.get("/other-parents", response_model=List[ParentDetails])
def view_other_parents(user_id: UUID = Depends(get_user_id_from_token)):
    parent = supabase.table("parents").select("group").eq("user_id", user_id).single().execute()
    if not parent.data or not parent.data.get("group"):
        raise HTTPException(status_code=404, detail="Parent group not found")

    others = supabase.table("parents").select("*").eq("group", parent.data["group"]).neq("user_id", user_id).execute()
    return others.data

# @router.get("/child/health")
# def get_child_health(child_email: str):
#     res = supabase.table("health_metrics").select("*").eq("email", child_email).order("created_at", desc=True).execute()
#     return res.data

# @router.get("/child/diet")
# def get_child_diet(child_email: str):
#     res = supabase.table("student_diet").select("*").eq("email", child_email).order("time", desc=True).execute()
#     return res.data

# @router.get("/child/meals")
# def get_child_meals(child_email: str):
#     res = supabase.table("meals").select("*").eq("email", child_email).order("time", desc=True).execute()
#     return res.data

# # -------------------------
# # Part 4: Parent Dashboard
# # -------------------------
# @router.get("/dashboard")
# def parent_dashboard(user_id: UUID = Depends(get_user_id_from_token)):
#     parent = supabase.table("parents").select("parent_id").eq("user_id", user_id).single().execute()
#     if not parent.data:
#         raise HTTPException(status_code=404, detail="Parent not found")
#     parent_id = parent.data['parent_id']

#     link_res = supabase.table("parent_children").select("child_id").eq("parent_id", parent_id).execute()
#     if not link_res.data:
#         return JSONResponse(content={"children": [], "alerts": []})

#     child_ids = [c['child_id'] for c in link_res.data]
#     summary = []
#     alerts = []

#     for child_id in child_ids:
#         user_res = supabase.table("users").select("email, full_name").eq("user_id", child_id).single().execute()
#         if not user_res.data:
#             continue
#         email = user_res.data["email"]
#         name = user_res.data["full_name"]

#         metric_res = supabase.table("health_metrics").select("*").eq("email", email).order("created_at", desc=True).limit(1).execute()
#         if not metric_res.data:
#             continue
#         metric = metric_res.data[0]

#         child_data = {
#             "name": name,
#             "email": email,
#             "weight": metric["weight"],
#             "bmi": metric["bmi"],
#             "bp": f"{metric['systolic']}/{metric['diastolic']}",
#             "blood_sugar": metric["blood_sugar"],
#             "heart_rate": metric["heart_rate"],
#             "notes": metric.get("notes", "")
#         }

#         child_alerts = []
#         if metric["blood_sugar"] > 130:
#             child_alerts.append(f"{name}: High blood sugar ({metric['blood_sugar']})")
#         if metric["systolic"] > 130 or metric["diastolic"] > 85:
#             child_alerts.append(f"{name}: Elevated blood pressure ({metric['systolic']}/{metric['diastolic']})")
#         if metric["heart_rate"] > 100 or metric["heart_rate"] < 50:
#             child_alerts.append(f"{name}: Irregular heart rate ({metric['heart_rate']})")

#         summary.append(child_data)
#         alerts.extend(child_alerts)

#     return {
#         "children": summary,
#         "alerts": alerts
#     }
