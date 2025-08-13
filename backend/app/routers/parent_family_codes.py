# app/routers/parent_family_codes.py
from fastapi import APIRouter, Depends, HTTPException, Body, Path
from fastapi.security import OAuth2PasswordBearer
from typing import List, Dict, Any
from uuid import UUID
from datetime import datetime, timedelta
from ..config import supabase

router = APIRouter(prefix="/parent/family/codes", tags=["parent-family-codes"])
oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/token")


def _get_user_id(token: str) -> UUID:
    auth = supabase.auth.get_user(token)
    if getattr(auth, "error", None) or not getattr(auth, "user", None):
        raise HTTPException(status_code=401, detail="Unauthorized")
    return auth.user.id


def _family_ids_for_head(user_id: str):
    res = (
        supabase.table("family_groups")
        .select("family_id")
        .eq("family_head_id", user_id)
        .execute()
    )
    return [row["family_id"] for row in (res.data or [])]


@router.get("/", response_model=List[Dict[str, Any]])
def list_family_codes(token: str = Depends(oauth2)):
    """List all invitation codes (target_type='family') for families headed by the caller."""
    user_id = _get_user_id(token)
    fam_ids = _family_ids_for_head(user_id)
    if not fam_ids:
        return []

    q = (
        supabase.table("invitation_codes")
        .select("*")
        .eq("target_type", "family")
        .in_("target_id", fam_ids)
        .order("created_at", desc=True)
        .execute()
    )
    return q.data or []


@router.post("/", response_model=Dict[str, Any])
def create_family_code(
    token: str = Depends(oauth2),
    target_id: UUID | None = Body(None),
    max_uses: int | None = Body(None),
    expires_in_hours: int | None = Body(None),
):
    """
    Create a new family invitation code.
    - If target_id is omitted, the first family headed by the user is used.
    - expires_in_hours -> converts to expires_at.
    """
    user_id = _get_user_id(token)
    fam_ids = _family_ids_for_head(user_id)
    if not fam_ids:
        raise HTTPException(400, "You don't head any family groups yet")

    target = str(target_id or fam_ids[0])

    # build code like FAM-XXXXXX-YYYYYY
    from random import choices
    import string as S
    code = f"FAM-{''.join(choices(S.ascii_uppercase+S.digits, k=6))}-{''.join(choices(S.ascii_uppercase+S.digits, k=6))}"

    expires_at = None
    if isinstance(expires_in_hours, int) and expires_in_hours > 0:
        expires_at = (datetime.utcnow() + timedelta(hours=expires_in_hours)).isoformat() + "Z"

    ins = (
        supabase.table("invitation_codes")
        .insert({
            "code": code,
            "target_type": "family",
            "target_id": target,
            "created_by": user_id,
            "max_uses": max_uses,
            "expires_at": expires_at,
        })
        .execute()
    )
    if not ins.data:
        raise HTTPException(400, "Failed to create code")
    return ins.data[0]


@router.delete("/{code_id}", response_model=Dict[str, Any])
def revoke_family_code(code_id: UUID = Path(...), token: str = Depends(oauth2)):
    """Soft-delete: mark a code as revoked (or delete if you prefer)."""
    user_id = _get_user_id(token)

    # ensure code belongs to one of the user's families
    code = (
        supabase.table("invitation_codes")
        .select("code_id,target_id")
        .eq("code_id", str(code_id))
        .single()
        .execute()
        .data
    )
    if not code:
        raise HTTPException(404, "Code not found")

    fam_ids = set(_family_ids_for_head(user_id))
    if code["target_id"] not in fam_ids:
        raise HTTPException(403, "Not authorized to revoke this code")

    upd = (
        supabase.table("invitation_codes")
        .update({"revoked_at": datetime.utcnow().isoformat() + "Z"})
        .eq("code_id", str(code_id))
        .execute()
    )
    if not upd.data:
        raise HTTPException(400, "Failed to revoke code")
    return {"revoked": True}
