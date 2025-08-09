from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from typing import Dict, Any, List

from ..config import supabase
from ..utils.profile_utils import get_user_id_from_token
from datetime import datetime, timezone

router = APIRouter(prefix="/connections", tags=["connections-activity"]) 
oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/token")


@router.get("/activity")
def get_connection_activity(token: str = Depends(oauth2)) -> Dict[str, List[Dict[str, Any]]]:
    """Return recent connection-related activities for the caller.

    Expects `connection_activity` table with columns:
      - activity_id, user_id, activity_type, message, created_at, status
    """
    user_id = get_user_id_from_token(token)
    res = (
        supabase.table("connection_activity")
        .select("*")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .limit(100)
        .execute()
    )
    rows = getattr(res, "data", []) or []
    activities = [
        {
            "activity_id": r.get("activity_id"),
            "type": r.get("activity_type"),
            "message": r.get("message"),
            "timestamp": r.get("created_at"),
            "status": r.get("status"),
        }
        for r in rows
    ]
    return {"activities": activities}


@router.get("/stats")
def get_connection_stats(token: str = Depends(oauth2)) -> Dict[str, Any]:
    """Return stats about connections, pending requests, and active invitations."""
    user_id = get_user_id_from_token(token)

    # Total connections and by type
    conn_res = (
        supabase.table("user_connections")
        .select("*")
        .or_(f"user_id_1.eq.{user_id},user_id_2.eq.{user_id}")
        .execute()
    )
    connections = getattr(conn_res, "data", []) or []
    total_connections = len(connections)
    teacher_connections = len([c for c in connections if c.get("connection_type") == "teacher_student"])
    parent_connections = len([c for c in connections if c.get("connection_type") == "parent_student" or c.get("connection_type") == "parent_parent"])
    family_connections = len([c for c in connections if c.get("connection_type") == "family"])

    # Pending requests: outbound + inbound (approver views)
    outbound_res = (
        supabase.table("join_requests")
        .select("*")
        .eq("requester_id", user_id)
        .eq("status", "pending")
        .execute()
    )
    outbound = getattr(outbound_res, "data", []) or []

    # inbound for approvers: family heads and teachers
    inbound = []
    # as family head: requests targeting any of my families
    fams = (
        supabase.table("family_groups")
        .select("family_id")
        .eq("family_head_id", user_id)
        .execute()
        .data
        or []
    )
    family_ids = [f["family_id"] for f in fams]
    if family_ids:
        fam_reqs = (
            supabase.table("join_requests")
            .select("*")
            .in_("target_id", family_ids)
            .eq("target_type", "family")
            .eq("status", "pending")
            .execute()
            .data
            or []
        )
        inbound.extend(fam_reqs)

    # as teacher: classroom requests targeting my user_id
    t_reqs = (
        supabase.table("join_requests")
        .select("*")
        .eq("target_type", "classroom")
        .eq("target_id", user_id)
        .eq("status", "pending")
        .execute()
        .data
        or []
    )
    inbound.extend(t_reqs)

    pending_requests = len(outbound) + len(inbound)

    # Active invitations: those created by me with remaining capacity and not expired
    # Fetch codes
    code_res = (
        supabase.table("invitation_codes").select("*").eq("created_by", user_id).execute()
    )
    codes = getattr(code_res, "data", []) or []
    # Build usage map
    code_ids = [c["code_id"] for c in codes]
    usage_map = {}
    if code_ids:
        reqs = (
            supabase.table("join_requests").select("code_id").in_("code_id", code_ids).execute()
        )
        for row in getattr(reqs, "data", []) or []:
            cid = row.get("code_id")
            if cid:
                usage_map[cid] = usage_map.get(cid, 0) + 1

    now = datetime.now(timezone.utc)
    active_invitations = 0
    for c in codes:
        uses = usage_map.get(c["code_id"], 0)
        expires_at = c.get("expires_at")
        is_expired = False
        if expires_at:
            try:
                from datetime import datetime as _dt
                exp_dt = _dt.fromisoformat(expires_at.replace('Z', '+00:00'))
                if exp_dt.tzinfo is None:
                    from datetime import timezone as _tz
                    exp_dt = exp_dt.replace(tzinfo=_tz.utc)
                is_expired = now >= exp_dt
            except Exception:
                is_expired = False
        max_uses = c.get("max_uses")
        is_exhausted = isinstance(max_uses, int) and uses >= max_uses if max_uses is not None else False
        if not is_expired and not is_exhausted:
            active_invitations += 1

    return {
        "total_connections": total_connections,
        "teacher_connections": teacher_connections,
        "parent_connections": parent_connections,
        "family_connections": family_connections,
        "pending_requests": pending_requests,
        "active_invitations": active_invitations,
    }
