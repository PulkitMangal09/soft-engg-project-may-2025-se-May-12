from fastapi import APIRouter, HTTPException, Depends, Path
from fastapi.security import OAuth2PasswordBearer
from typing import List, Dict, Any
from uuid import UUID
from datetime import datetime

from ..config import supabase

router = APIRouter(prefix="/parent/requests", tags=["parent-requests"])
oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/token")


def get_user_id(token: str) -> str:
    auth = supabase.auth.get_user(token)
    if getattr(auth, "error", None):
        raise HTTPException(status_code=401, detail="Invalid token")
    return auth.user.id


@router.get("/", response_model=List[Dict[str, Any]])
def list_requests(token: str = Depends(oauth2)):
    """
    List all pending 'family' join requests for families this user heads.
    """
    user_id = get_user_id(token)

    # 1) find all families where I'm head
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

    # 2) fetch pending join_requests for those families
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


@router.post("/{request_id}/approve", response_model=Dict[str, Any])
def approve_request(
    request_id: UUID = Path(..., description="The join_request ID to approve"),
    token: str = Depends(oauth2),
):
    """
    Approve a pending family-join request.
    """
    user_id = get_user_id(token)

    # fetch the request
    r = supabase.table("join_requests")\
        .select("*")\
        .eq("request_id", str(request_id))\
        .single()\
        .execute()
    req = r.data
    if not req or req["status"] != "pending":
        raise HTTPException(status_code=404, detail="Pending request not found")

    family_id = req["target_id"]
    requester_id = req["requester_id"]

    # ensure I'm actually the head of this family
    fam = (
        supabase
        .table("family_groups")
        .select("family_head_id")
        .eq("family_id", family_id)
        .single()
        .execute()
        .data
    )
    if not fam or fam["family_head_id"] != user_id:
        raise HTTPException(status_code=403, detail="Not family head")

    # mark request approved
    supabase.table("join_requests").update({
        "status": "approved",
        "responded_at": datetime.utcnow().isoformat(),
        "responded_by": user_id,
    }).eq("request_id", str(request_id)).execute()

    # insert into family_members
    supabase.table("family_members").insert({
        "family_id":       family_id,
        "user_id":         requester_id,
        "role":            req["relationship_type"],
    }).execute()

    return {"request_id": request_id, "status": "approved"}


@router.post("/{request_id}/reject", response_model=Dict[str, Any])
def reject_request(
    request_id: UUID = Path(..., description="The join_request ID to reject"),
    token: str = Depends(oauth2),
):
    """
    Reject a pending family-join request.
    """
    user_id = get_user_id(token)

    # fetch the request
    r = supabase.table("join_requests")\
        .select("*")\
        .eq("request_id", str(request_id))\
        .single()\
        .execute()
    req = r.data
    if not req or req["status"] != "pending":
        raise HTTPException(status_code=404, detail="Pending request not found")

    family_id = req["target_id"]

    # ensure I'm actually the head of this family
    fam = (
        supabase
        .table("family_groups")
        .select("family_head_id")
        .eq("family_id", family_id)
        .single()
        .execute()
        .data
    )
    if not fam or fam["family_head_id"] != user_id:
        raise HTTPException(status_code=403, detail="Not family head")

    # mark request rejected
    supabase.table("join_requests").update({
        "status": "rejected",
        "responded_at": datetime.utcnow().isoformat(),
        "responded_by": user_id,
    }).eq("request_id", str(request_id)).execute()

    return {"request_id": request_id, "status": "rejected"}
