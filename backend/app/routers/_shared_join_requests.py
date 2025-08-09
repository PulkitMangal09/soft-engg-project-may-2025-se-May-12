from typing import List, Dict, Any, Optional
from uuid import UUID
from datetime import datetime, timezone
from fastapi import HTTPException

from ..config import supabase


def is_family_head(user_id: str, family_id: str) -> bool:
    r = (
        supabase.table("family_groups")
        .select("family_head_id")
        .eq("family_id", family_id)
        .single()
        .execute()
    )
    data = getattr(r, "data", None)
    return bool(data and data.get("family_head_id") == user_id)


def list_pending_for_family_head(user_id: str) -> List[Dict[str, Any]]:
    fams = (
        supabase
        .table("family_groups")
        .select("family_id")
        .eq("family_head_id", user_id)
        .execute()
        .data
        or []
    )
    family_ids = [f["family_id"] for f in fams]
    if not family_ids:
        return []

    reqs = (
        supabase
        .table("join_requests")
        .select("*")
        .in_("target_id", family_ids)
        .eq("target_type", "family")
        .eq("status", "pending")
        .execute()
        .data
        or []
    )
    return reqs


def _get_request(request_id: str) -> Optional[Dict[str, Any]]:
    r = (
        supabase.table("join_requests")
        .select("*")
        .eq("request_id", request_id)
        .single()
        .execute()
    )
    return getattr(r, "data", None)


def approve_family_join_request(request_id: str, approver_id: str) -> Dict[str, Any]:
    req = _get_request(request_id)
    if not req or req.get("status") != "pending":
        raise HTTPException(status_code=404, detail="Pending request not found")

    if req.get("target_type") != "family":
        raise HTTPException(status_code=400, detail="Not a family join request")

    family_id = req["target_id"]
    requester_id = req["requester_id"]

    if not is_family_head(approver_id, family_id):
        raise HTTPException(status_code=403, detail="Not family head")

    # mark approved
    supabase.table("join_requests").update({
        "status": "approved",
        "responded_at": datetime.now(timezone.utc).isoformat(),
        "responded_by": approver_id,
    }).eq("request_id", request_id).execute()

    # ensure membership exists
    exists = (
        supabase.table("family_members")
        .select("member_id")
        .eq("family_id", family_id)
        .eq("user_id", requester_id)
        .execute()
        .data
    )
    if not exists:
        supabase.table("family_members").insert({
            "family_id": family_id,
            "user_id": requester_id,
            "role": req.get("relationship_type"),
        }).execute()

    return {"request_id": request_id, "status": "approved"}


def reject_family_join_request(request_id: str, approver_id: str) -> Dict[str, Any]:
    req = _get_request(request_id)
    if not req or req.get("status") != "pending":
        raise HTTPException(status_code=404, detail="Pending request not found")

    if req.get("target_type") != "family":
        raise HTTPException(status_code=400, detail="Not a family join request")

    family_id = req["target_id"]

    if not is_family_head(approver_id, family_id):
        raise HTTPException(status_code=403, detail="Not family head")

    supabase.table("join_requests").update({
        "status": "rejected",
        "responded_at": datetime.now(timezone.utc).isoformat(),
        "responded_by": approver_id,
    }).eq("request_id", request_id).execute()

    return {"request_id": request_id, "status": "rejected"}
