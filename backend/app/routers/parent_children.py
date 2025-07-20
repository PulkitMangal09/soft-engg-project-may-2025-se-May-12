# routers/parent.py
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.security import OAuth2PasswordBearer
from typing import List, Optional
from pydantic import BaseModel
from uuid import UUID
from ..config import supabase
from ..models import ChildHealthSnapshot, ChildLinkRequest, ParentDetails, HealthMetric, ChildDietLog, Meal_Log, UpdateChildLink
from fastapi.responses import JSONResponse
import jwt
from datetime import datetime

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
        user_res = supabase.table("students").select("name").eq("student_id", child_id).single().execute()
        if not user_res.data:
            continue
        name = user_res.data['name']
        metric_res = supabase.table("health_metrics").select("*").eq("student_id", child_id).order("created_at", desc=True).limit(1).execute()
        if not metric_res.data:
            continue
        m = metric_res.data[0]
        snapshots.append(ChildHealthSnapshot(
            full_name=name,
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

@router.patch("/children/relationship", response_model=dict)
def update_child_relationship(
    update: UpdateChildLink,
    user_id: UUID = Depends(get_user_id_from_token)
):
    parent = supabase.table("parents").select("parent_id").eq("user_id", user_id).single().execute()
    if not parent.data:
        raise HTTPException(status_code=404, detail="Parent not found")

    parent_id = parent.data["parent_id"]
    res = supabase.table("parent_children").update({
        "relationship": update.relationship
    }).eq("parent_id", str(parent_id)).eq("child_id", str(update.child_id)).execute()

    if not res.data:
        raise HTTPException(status_code=404, detail="No link found to update")

    return {"message": "Relationship updated"}

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

@router.get("/other-parents", response_model=List[ParentDetails])
def view_other_parents(user_id: UUID = Depends(get_user_id_from_token)):
    parent = supabase.table("parents").select("group").eq("user_id", user_id).single().execute()
    if not parent.data or not parent.data.get("group"):
        raise HTTPException(status_code=404, detail="Parent group not found")

    others = supabase.table("parents").select("*").eq("group", parent.data["group"]).neq("user_id", user_id).execute()
    return others.data


@router.get("/child/health", response_model=List[HealthMetric])
def get_child_health_data(
    child_id: str,
    parent_email: str = Depends(get_email_from_token)
):
    # Validate parent-child relationship
    parent_res = supabase.table("users").select("user_id").eq("email", parent_email).execute()
    if not parent_res.data:
        raise HTTPException(status_code=404, detail="Parent not found")

    user_id = parent_res.data[0]['user_id']
    parent = supabase.table("parents").select("parent_id").eq("user_id", user_id).execute()
    if not parent.data:
        raise HTTPException(status_code=403, detail="Not authorized as a parent")

    parent_id = parent.data[0]['parent_id']
    link = supabase.table("parent_children").select("*").eq("parent_id", parent_id).eq("child_id", child_id).execute()
    if not link.data:   
        raise HTTPException(status_code=403, detail="No access to this child's data")

    # Fetch health metrics
    metrics = supabase.table("health_metrics").select("*").eq("student_id", child_id).order("created_at", desc=True).execute()
    return metrics.data

@router.get("/children/diet", response_model=List[ChildDietLog])
def view_children_diet(parent_email: str = Depends(get_email_from_token)):
    # Step 1: Resolve user_id from parent_email
    user_res = supabase.table("users").select("user_id").eq("email", parent_email).execute()
    if not user_res.data:
        raise HTTPException(status_code=404, detail="User not found")
    user_id = user_res.data[0]["user_id"]

    # Step 2: Get parent_id from parents
    parent_res = supabase.table("parents").select("parent_id").eq("user_id", user_id).execute()
    if not parent_res.data:
        raise HTTPException(status_code=404, detail="Parent not found")
    parent_id = parent_res.data[0]["parent_id"]

    # Step 3: Get child_ids
    children_res = supabase.table("parent_children").select("child_id").eq("parent_id", parent_id).execute()
    if not children_res.data:
        return []

    child_ids = [child["child_id"] for child in children_res.data]

    # Step 4: Fetch diet data for all children
    diet_logs = []
    for child_id in child_ids:
        child = supabase.table("students").select("email, name").eq("student_id", child_id).execute()
        child_email = child.data[0]['email']    
        child_name = child.data[0]['name']    
        diet_res = (
            supabase.table("student_diet")
            .select("time, water_glasses, sodium, sugar")
            .eq("student_id", child_id)
            .order("time", desc=True)
            .execute()
        )
        for entry in diet_res.data:
            diet_logs.append({
                "child_name": child_name,
                "child_id": child_id,
                "date": entry["time"],
                "water_glasses": entry["water_glasses"],
                "sodium": entry["sodium"],
                "sugar": entry["sugar"]
            })

    return diet_logs

@router.get("/child/meals", response_model=List[Meal_Log])
def get_child_meal_logs(
    child_id: str,
    parent_email: str = Depends(get_email_from_token)
):
    # Validate parent-child relationship (same as above)
    parent_res = supabase.table("users").select("user_id").eq("email", parent_email).execute()
    if not parent_res.data:
        raise HTTPException(status_code=404, detail="Parent not found")

    user_id = parent_res.data[0]['user_id']
    parent = supabase.table("parents").select("parent_id").eq("user_id", user_id).execute()
    if not parent.data:
        raise HTTPException(status_code=403, detail="Not authorized as a parent")

    parent_id = parent.data[0]['parent_id']
    link = supabase.table("parent_children").select("*").eq("parent_id", parent_id).eq("child_id", child_id).execute()
    if not link.data:
        raise HTTPException(status_code=403, detail="No access to this child's data")
        
    # Fetch meal logs
    meals = supabase.table("meals").select("*").eq("student_id", child_id).order("time", desc=True).execute()
    return meals.data
