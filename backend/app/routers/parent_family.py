from fastapi import APIRouter, HTTPException, Depends, Path, Body
from fastapi.security import OAuth2PasswordBearer
from typing import List, Dict, Any
from uuid import UUID
from datetime import datetime

from ..config import supabase

router = APIRouter(prefix="/parent/family", tags=["parent-family"])
oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/token")


def get_user_id(token: str) -> UUID:
    auth = supabase.auth.get_user(token)
    if getattr(auth, "error", None):
        raise HTTPException(status_code=401, detail="Unauthorized")
    return auth.user.id


@router.get("/overview", response_model=Dict[str, Any])
def family_overview(token: str = Depends(oauth2)):
    """Return summary cards for tasks, finance, health across family."""
    user_id = get_user_id(token)

    # count children in families you head
    counts = (
        supabase
        .rpc("count_family_children", {"head_id": user_id})
        .execute()
        .data
    )
    # you could also do raw SQL or two queries against family_groups & family_members

    return {
        "children": counts[0]["child_count"],
        "pendingRequests": (
            supabase.table("join_requests")
            .select("count(*)", count="exact")
            .eq("target_type", "family")
            .in_("target_id",
                 [f["family_id"] for f in supabase
                    .table("family_groups")
                    .select("family_id")
                    .eq("family_head_id", user_id)
                    .execute()
                    .data or []])
            .eq("status", "pending")
            .execute()
            .data[0]["count"]
        ),
        # similarly for tasks/finance/health across all your children...
    }


@router.post("/groups", response_model=Dict[str, Any])
def create_family_group(
    name: str = Body(..., embed=True),
    description: str = Body(None, embed=True),
    token: str = Depends(oauth2),
):
    """Create a new family group (you become the head)."""
    user_id = get_user_id(token)
    payload = {
        "family_name": name,
        "description":  description,
        "family_head_id": user_id,
    }
    resp = supabase.table("family_groups").insert(payload).execute()
    if not resp.data:
        raise HTTPException(400, "Could not create family group")
    return resp.data[0]


@router.get("/groups", response_model=List[Dict[str, Any]])
def list_family_groups(token: str = Depends(oauth2)):
    """List all family groups you head."""
    user_id = get_user_id(token)
    resp = (
        supabase
        .table("family_groups")
        .select("*")
        .eq("family_head_id", user_id)
        .execute()
    )
    return resp.data or []


@router.get("/groups/{group_id}", response_model=Dict[str, Any])
def get_family_group(
    group_id: UUID = Path(...),
    token: str    = Depends(oauth2),
):
    """Get details (and members) of a single family group."""
    user_id = get_user_id(token)

    # ensure you’re the head
    grp = (
        supabase
        .table("family_groups")
        .select("*")
        .eq("family_id", str(group_id))
        .single()
        .execute()
        .data
    )
    if not grp or grp["family_head_id"] != user_id:
        raise HTTPException(404, "Family not found")

    members = (
        supabase
        .table("family_members")
        .select("user_id, role, joined_at")
        .eq("family_id", str(group_id))
        .execute()
        .data
    )
    grp["members"] = members or []
    return grp


@router.post("/groups/{group_id}/add/{child_id}", response_model=Dict[str, Any])
def add_family_member(
    group_id: UUID = Path(...),
    child_id: UUID = Path(...),
    role: str      = Body("child", embed=True),
    token: str     = Depends(oauth2),
):
    """Add a child (or guardian) to your family group."""
    user_id = get_user_id(token)

    # verify you’re head
    grp = (
        supabase
        .table("family_groups")
        .select("family_head_id")
        .eq("family_id", str(group_id))
        .single()
        .execute()
        .data
    )
    if not grp or grp["family_head_id"] != user_id:
        raise HTTPException(403, "Not authorized")

    # insert member
    payload = {
        "family_id": str(group_id),
        "user_id":   str(child_id),
        "role":      role,
    }
    resp = supabase.table("family_members").insert(payload).execute()
    if not resp.data:
        raise HTTPException(400, "Could not add member")
    return resp.data[0]


@router.delete("/groups/{group_id}/remove/{child_id}", response_model=Dict[str, Any])
def remove_family_member(
    group_id: UUID = Path(...),
    child_id: UUID = Path(...),
    token: str     = Depends(oauth2),
):
    """Remove a member from your family group."""
    user_id = get_user_id(token)

    # verify head
    grp = (
        supabase
        .table("family_groups")
        .select("family_head_id")
        .eq("family_id", str(group_id))
        .single()
        .execute()
        .data
    )
    if not grp or grp["family_head_id"] != user_id:
        raise HTTPException(403, "Not authorized")

    supabase.table("family_members") \
        .delete() \
        .eq("family_id", str(group_id)) \
        .eq("user_id",   str(child_id)) \
        .execute()

    return {"removed": True}
