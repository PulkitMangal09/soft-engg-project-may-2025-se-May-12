from fastapi import APIRouter, HTTPException, Depends, Path
from fastapi.security import OAuth2PasswordBearer
from typing import List, Dict, Any
from uuid import UUID
from datetime import datetime

from ..config import supabase
from ..utils.profile_utils import get_user_id_from_token
from ._shared_join_requests import (
    list_pending_for_family_head,
    approve_family_join_request,
    reject_family_join_request,
)

router = APIRouter(prefix="/parent/requests", tags=["parent-requests"])
oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/token")


@router.get("/", response_model=List[Dict[str, Any]])
def list_requests(token: str = Depends(oauth2)):
    """List all pending 'family' join requests for families this user heads."""
    user_id = get_user_id_from_token(token)
    reqs = list_pending_for_family_head(user_id)
    # Enrich with requester_name from users table
    try:
        requester_ids = [r.get("requester_id") for r in reqs if r.get("requester_id")]
        if requester_ids:
            users_res = (
                supabase
                .table("users")
                .select("user_id, full_name, email")
                .in_("user_id", requester_ids)
                .execute()
            )
            users = getattr(users_res, "data", None) or []
            by_id = {u["user_id"]: u for u in users}
            for r in reqs:
                u = by_id.get(r.get("requester_id")) or {}
                name = u.get("full_name") or u.get("email")
                if name:
                    r["requester_name"] = name
    except Exception:
        # If enrichment fails, return base requests
        pass
    return reqs


@router.post("/{request_id}/approve", response_model=Dict[str, Any])
def approve_request(
    request_id: UUID = Path(..., description="The join_request ID to approve"),
    token: str = Depends(oauth2),
):
    """Approve a pending family-join request."""
    user_id = get_user_id_from_token(token)
    result = approve_family_join_request(str(request_id), user_id)
    return {"request_id": request_id, **result}


@router.post("/{request_id}/reject", response_model=Dict[str, Any])
def reject_request(
    request_id: UUID = Path(..., description="The join_request ID to reject"),
    token: str = Depends(oauth2),
):
    """Reject a pending family-join request."""
    user_id = get_user_id_from_token(token)
    result = reject_family_join_request(str(request_id), user_id)
    return {"request_id": request_id, **result}
