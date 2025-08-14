from fastapi import APIRouter, Depends, Query, HTTPException, Body
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from ..config import supabase
from datetime import datetime, timedelta

router = APIRouter(prefix="/parent/dashboard", tags=["parent-dashboard"])
oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/token")

@router.get("/")
def get_parent_dashboard(
    token: str = Depends(oauth2),
    child_id: Optional[str] = Query(None)
):
    """
    Aggregated parent dashboard endpoint. Returns summary, children, alerts, attention, achievements.
    If child_id is provided, filters all metrics for that child only.
    """
    # 1. Auth: Get parent user
    user_response = supabase.auth.get_user(token)
    if not user_response or not user_response.user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    parent_user_id = user_response.user.id

    # 2. Resolve families via family_groups/family_members
    head_resp = (
        supabase.table("family_groups")
        .select("family_id")
        .eq("family_head_id", parent_user_id)
        .eq("is_active", True)
        .execute()
    )
    head_family_ids = {row["family_id"] for row in (head_resp.data or [])}

    member_resp = (
        supabase.table("family_members")
        .select("family_id, role, is_active")
        .eq("user_id", parent_user_id)
        .eq("is_active", True)
        .execute()
    )
    member_family_ids = {row["family_id"] for row in (member_resp.data or []) if row.get("role") in ("head", "parent")}

    family_ids = list(head_family_ids.union(member_family_ids))

    # 3. Get children (all or specific) from family memberships
    children = []
    if family_ids:
        fm_query = (
            supabase.table("family_members")
            .select("user_id, role, is_active, family_id")
            .in_("family_id", family_ids)
            .eq("role", "child")
            .eq("is_active", True)
        )
        if child_id:
            fm_query = fm_query.eq("user_id", child_id)
        fm_resp = fm_query.execute()
        children = list({row["user_id"] for row in (fm_resp.data or [])})
    
    # 4. Get children details (from users table)
    children_details = []
    if children:
        users_resp = (
            supabase.table("users")
            .select("user_id, full_name, email, created_at, user_type")
            .in_("user_id", children)
            .execute()
        )
        users = users_resp.data or []
        for u in users:
            children_details.append({
                "student_id": u.get("user_id"),
                "name": u.get("full_name") or u.get("email") or "Student",
                "email": u.get("email"),
                "created_at": u.get("created_at"),
                "avatar_url": f"https://randomuser.me/api/portraits/lego/{hash(u.get('user_id')) % 10 + 1}.jpg",
            })

    # 5. Summary stats
    summary = {
        "childrenCount": len(children_details),
        "pendingRequests": 0,  # To be filled below
        "activeTasks": 0,      # To be filled below
        "financeGoals": 0,     # To be filled below
    }

    # 6. Pending join/access requests
    # requests_resp = supabase.table("parent_requests").select("*").eq("parent_id", parent_id).eq("status", "pending").execute()
    # summary["pendingRequests"] = len(requests_resp.data) if requests_resp.data else 0

    # 7. Active tasks for children
    if children:
        tasks_resp = supabase.table("tasks").select("*").in_("assigned_to", children).in_("status", ["pending", "in_progress"]).execute()
        summary["activeTasks"] = len(tasks_resp.data) if tasks_resp.data else 0
    else:
        summary["activeTasks"] = 0

    # 8. Finance goals count
    if children:
        finance_resp = supabase.table("savings_goals").select("*").in_("student_id", children).execute()
        summary["financeGoals"] = len(finance_resp.data) if finance_resp.data else 0
    else:
        summary["financeGoals"] = 0

    # 8. Alerts (e.g., health)
    alerts = []
    if children:
        # Example: critical health alerts (e.g., blood sugar > 180)
        health_resp = supabase.table("health_metrics").select("student_id, created_at, blood_sugar, systolic, diastolic").in_("student_id", children).order("created_at", desc=True).limit(10).execute()
        for entry in health_resp.data or []:
            if entry.get("blood_sugar") and entry["blood_sugar"] > 180:
                alerts.append({
                    "type": "health",
                    "message": f"{entry['student_id']} blood sugar elevated ({entry['blood_sugar']} mg/dL)",
                    "student_id": entry["student_id"],
                    "created_at": entry["created_at"]
                })
            # Add more alert types as needed

    # 9. Attention Needed (e.g., overdue tasks, low engagement)
    attention_needed = []
    if children:
        now = datetime.utcnow().isoformat()
        # Overdue tasks
        overdue_resp = supabase.table("tasks").select("task_id, title, due_date, assigned_to").in_("assigned_to", children).in_("status", ["pending", "in_progress"]).lt("due_date", now).execute()
        for t in overdue_resp.data or []:
            attention_needed.append({
                "student_id": t["assigned_to"],
                "issue": f"Overdue task: {t['title']} (due {t['due_date']})"
            })
        # Low engagement: e.g., <2 tasks completed in last 7 days
        seven_days_ago = (datetime.utcnow() - timedelta(days=7)).isoformat()
        completions_resp = supabase.table("task_completions").select("student_id, completed_at").in_("student_id", children).gte("completed_at", seven_days_ago).execute()
        completed_count = {}
        for c in completions_resp.data or []:
            sid = c["student_id"]
            completed_count[sid] = completed_count.get(sid, 0) + 1
        for sid in children:
            if completed_count.get(sid, 0) < 2:
                attention_needed.append({
                    "student_id": sid,
                    "issue": "Low engagement (less than 2 tasks completed in last 7 days)"
                })

    # 10. Achievements (e.g., perfect completion, improvement)
    achievements = []
    if children:
        # Example: perfect completion in last week
        for child in children:
            # Get all tasks assigned in last 7 days
            week_ago = (datetime.utcnow() - timedelta(days=7)).isoformat()
            tasks_week = supabase.table("tasks").select("task_id").eq("assigned_to", child).gte("created_at", week_ago).execute().data or []
            completions_week = supabase.table("task_completions").select("task_id").eq("student_id", child).gte("completed_at", week_ago).execute().data or []
            if tasks_week and len(completions_week) == len(tasks_week):
                achievements.append({
                    "student_id": child,
                    "achievement": "Perfect task completion this week"
                })
        # Example: improvement (score increase)
        # (Assume you have a 'score' field in task_completions)
        for child in children:
            scores_resp = supabase.table("task_completions").select("scores, completed_at").eq("student_id", child).order("completed_at", desc=True).limit(2).execute()
            scores = [r["score"] for r in scores_resp.data or [] if r.get("score") is not None]
            if len(scores) == 2 and scores[0] - scores[1] >= 15:
                achievements.append({
                    "student_id": child,
                    "achievement": "Significant improvement in task scores"
                })

    # Parent details: derive minimal info from users and family_groups (head role)
    user_resp = supabase.table("users").select("user_id, full_name").eq("user_id", parent_user_id).single().execute()
    parent_details = {
        "user_id": parent_user_id,
        "name": (user_resp.data or {}).get("full_name") or "Parent",
        "group": "Family",
        "is_head": bool(head_family_ids),
        "description": "Parent dashboard for managing children's activities and health",
        "is_active": True,
        "created_at": (user_resp.data or {}).get("created_at"),
        "updated_at": (user_resp.data or {}).get("created_at"),
    }

    # 11. Compose response
    return {
        "parent_details": parent_details,
        "summary": summary,
        "children": children_details,
        "criticalAlerts": alerts,
        "attentionNeeded": attention_needed,
        "achievements": achievements
    }

@router.get("/tasks")
def get_parent_tasks(
    token: str = Depends(oauth2),
    status: Optional[str] = Query(None),
    child_id: Optional[str] = Query(None),
    sortBy: Optional[str] = Query("created_at")
):
    """
    Returns all tasks for the parent's children, with optional filtering by status, child_id, and sorting.
    """
    user_response = supabase.auth.get_user(token)
    if not user_response or not user_response.user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    parent_user_id = user_response.user.id

    # Resolve families
    head_resp = (
        supabase.table("family_groups")
        .select("family_id")
        .eq("family_head_id", parent_user_id)
        .eq("is_active", True)
        .execute()
    )
    head_family_ids = {row["family_id"] for row in (head_resp.data or [])}
    member_resp = (
        supabase.table("family_members")
        .select("family_id, role, is_active")
        .eq("user_id", parent_user_id)
        .eq("is_active", True)
        .execute()
    )
    member_family_ids = {row["family_id"] for row in (member_resp.data or []) if row.get("role") in ("head", "parent")}
    family_ids = list(head_family_ids.union(member_family_ids))

    # Resolve children
    children = []
    if family_ids:
        fm_query = (
            supabase.table("family_members")
            .select("user_id, role, is_active")
            .in_("family_id", family_ids)
            .eq("role", "child")
            .eq("is_active", True)
        )
        if child_id:
            fm_query = fm_query.eq("user_id", child_id)
        fm_resp = fm_query.execute()
        children = list({row["user_id"] for row in (fm_resp.data or [])})
    if not children:
        return []
    query = supabase.table("tasks").select("*")
    query = query.in_("assigned_to", children)
    if status:
        query = query.eq("status", status)
    if sortBy:
        query = query.order(sortBy, desc=True)
    else:
        query = query.order("created_at", desc=True)
    response = query.execute()  
    return response.data

@router.get("/finance/transactions")
def get_parent_finance_transactions(
    token: str = Depends(oauth2),
    child_id: Optional[str] = Query(None),
    from_date: Optional[str] = Query(None, description="YYYY-MM-DD"),
    to_date: Optional[str] = Query(None, description="YYYY-MM-DD"),
    type: Optional[str] = Query(None, description="Income or Expense"),
    q: Optional[str] = Query(None, description="search text for category/note"),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=200),
):
    """Return transactions for the parent's children (from family groups), with optional filters.

    Resolution logic:
    - Identify families where the requester is head (family_head_id) OR a member with role in ('head','parent') and is_active.
    - Children are users in those families with role = 'child' and is_active.
    - child_id, if provided, must be within this set.
    """
    # Auth: user id
    user_response = supabase.auth.get_user(token)
    if not user_response or not user_response.user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    user_id = user_response.user.id

    # Families where user is head
    head_resp = (
        supabase.table("family_groups")
        .select("family_id")
        .eq("family_head_id", user_id)
        .eq("is_active", True)
        .execute()
    )
    head_family_ids = {row["family_id"] for row in (head_resp.data or [])}

    # Families where user is a parent/head member
    member_resp = (
        supabase.table("family_members")
        .select("family_id, role, is_active")
        .eq("user_id", user_id)
        .eq("is_active", True)
        .execute()
    )
    member_family_ids = {row["family_id"] for row in (member_resp.data or []) if row.get("role") in ("head", "parent")}

    family_ids = list(head_family_ids.union(member_family_ids))
    if not family_ids:
        return {"items": [], "page": page, "limit": limit, "total": 0}

    # Resolve children (role='child') within these families
    children_query = (
        supabase.table("family_members")
        .select("user_id, family_id, role, is_active")
        .in_("family_id", family_ids)
        .eq("role", "child")
        .eq("is_active", True)
    )
    if child_id:
        children_query = children_query.eq("user_id", child_id)
    children_resp = children_query.execute()
    children = list({row["user_id"] for row in (children_resp.data or [])})
    if not children:
        return {"items": [], "page": page, "limit": limit, "total": 0}

    # Build base query using transactions.student_id = users.user_id
    query = (
        supabase.table("transactions")
        .select("transaction_id, type, amount, transaction_date, category, note, student_id")
        .in_("student_id", children)
    )

    # Date range filter
    if from_date:
        query = query.gte("transaction_date", from_date)
    if to_date:
        query = query.lte("transaction_date", to_date)

    # Type filter
    if type in ("Income", "Expense"):
        query = query.eq("type", type)

    # Order newest first
    query = query.order("transaction_date", desc=True)

    # Execute (Supabase PostgREST does not support server-side pagination easily without RPC; do client-side slice)
    resp = query.execute()
    rows = resp.data or []

    # Text filter (category/note)
    if q:
        q_lower = q.lower()
        rows = [r for r in rows if (str(r.get("category") or "").lower().find(q_lower) >= 0) or (str(r.get("note") or "").lower().find(q_lower) >= 0)]

    total = len(rows)
    start = (page - 1) * limit
    end = start + limit
    items = rows[start:end]

    return {"items": items, "page": page, "limit": limit, "total": total}

@router.get("/health/alerts")
def get_parent_health_alerts(
    token: str = Depends(oauth2),
    severity: Optional[str] = Query(None),
    child_id: Optional[str] = Query(None)
):
    """
    Returns all active health alerts for the parent's children, with optional filtering by severity and child_id.
    """
    user_response = supabase.auth.get_user(token)
    if not user_response or not user_response.user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    parent_user_id = user_response.user.id
    parent_resp = supabase.table("parents").select("parent_id").eq("user_id", parent_user_id).single().execute()
    if not parent_resp.data:
        raise HTTPException(status_code=404, detail="Parent not found")
    parent_id = parent_resp.data["parent_id"]
    children_query = supabase.table("parent_children").select("child_id").eq("parent_id", parent_id)
    if child_id:
        children_query = children_query.eq("child_id", child_id)
    children_resp = children_query.execute()
    children = [c["child_id"] for c in children_resp.data] if children_resp.data else []
    if not children:
        return []
    alerts = []
    health_resp = supabase.table("health_metrics").select("student_id, created_at, blood_sugar, systolic, diastolic").in_("student_id", children).order("created_at", desc=True).limit(20).execute()
    for entry in health_resp.data or []:
        if severity == "critical":
            if entry.get("blood_sugar") and entry["blood_sugar"] > 180:
                alerts.append({
                    "type": "health",
                    "message": f"{entry['student_id']} blood sugar elevated ({entry['blood_sugar']} mg/dL)",
                    "student_id": entry["student_id"],
                    "created_at": entry["created_at"]
                })
        else:
            if entry.get("blood_sugar") and entry["blood_sugar"] > 140:
                alerts.append({
                    "type": "health",
                    "message": f"{entry['student_id']} blood sugar high ({entry['blood_sugar']} mg/dL)",
                    "student_id": entry["student_id"],
                    "created_at": entry["created_at"]
                })
    return alerts

@router.get("/finance/goals")
def get_parent_finance_goals(
    token: str = Depends(oauth2),
    status: Optional[str] = Query(None),
    child_id: Optional[str] = Query(None)
):
    """
    Returns all savings goals for the parent's children, with optional filtering by status and child_id.
    """
    user_response = supabase.auth.get_user(token)
    if not user_response or not user_response.user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    parent_user_id = user_response.user.id

    # Resolve families
    head_resp = (
        supabase.table("family_groups")
        .select("family_id")
        .eq("family_head_id", parent_user_id)
        .eq("is_active", True)
        .execute()
    )
    head_family_ids = {row["family_id"] for row in (head_resp.data or [])}
    member_resp = (
        supabase.table("family_members")
        .select("family_id, role, is_active")
        .eq("user_id", parent_user_id)
        .eq("is_active", True)
        .execute()
    )
    member_family_ids = {row["family_id"] for row in (member_resp.data or []) if row.get("role") in ("head", "parent")}
    family_ids = list(head_family_ids.union(member_family_ids))

    # Resolve children
    children = []
    if family_ids:
        fm_query = (
            supabase.table("family_members")
            .select("user_id, role, is_active")
            .in_("family_id", family_ids)
            .eq("role", "child")
            .eq("is_active", True)
        )
        if child_id:
            fm_query = fm_query.eq("user_id", child_id)
        fm_resp = fm_query.execute()
        children = list({row["user_id"] for row in (fm_resp.data or [])})
    if not children:
        return []
    query = supabase.table("savings_goals").select("*").in_("student_id", children)
    if status:
        query = query.eq("status", status)
    response = query.execute()
    return response.data

@router.get("/family/join-requests")
def get_family_join_requests(token: str = Depends(oauth2)):
    """
    Returns a list of pending join requests to the family group.
    """
    user_response = supabase.auth.get_user(token)
    if not user_response or not user_response.user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    parent_user_id = user_response.user.id
    parent_resp = supabase.table("parents").select("parent_id, group").eq("user_id", parent_user_id).single().execute()
    if not parent_resp.data or not parent_resp.data.get("group"):
        raise HTTPException(status_code=404, detail="Parent group not found")
    group = parent_resp.data["group"]
    requests_resp = supabase.table("join_requests") \
        .select("*") \
        .eq("target_type", "family") \
        .eq("target_id", group) \
        .eq("status", "pending") \
        .execute()
    return requests_resp.data or []

@router.post("/family/join-requests/respond")
def respond_family_join_request(
    token: str = Depends(oauth2),
    body: dict = Body(...)
):
    """
    Accept or reject a join request. Body: { "request_id": "<uuid>", "action": "accept" | "reject" }
    """
    user_response = supabase.auth.get_user(token)
    if not user_response or not user_response.user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    parent_user_id = user_response.user.id
    request_id = body.get("request_id")
    action = body.get("action")
    if not request_id or action not in ("accept", "reject"):
        raise HTTPException(status_code=400, detail="Invalid request body")
    req_resp = supabase.table("join_requests").select("*").eq("request_id", request_id).single().execute()
    if not req_resp.data:
        raise HTTPException(status_code=404, detail="Join request not found")
    new_status = "accepted" if action == "accept" else "rejected"
    update_resp = supabase.table("join_requests").update({
        "status": new_status,
        "responded_at": datetime.utcnow(),
        "responded_by": parent_user_id
    }).eq("request_id", request_id).execute()
    if update_resp.error:
        raise HTTPException(status_code=400, detail=update_resp.error.message)
    return {"message": f"Request {action}ed"}