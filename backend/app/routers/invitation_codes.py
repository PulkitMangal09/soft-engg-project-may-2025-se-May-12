from fastapi import APIRouter, HTTPException, Depends, Response
from fastapi.security import OAuth2PasswordBearer
from typing import Dict, Any, Optional
from uuid import UUID
from datetime import datetime, timezone
import random
import string

from ..config import supabase
from ..utils.profile_utils import get_user_id_from_token, get_user_type
from ..models import InvitationCodeCreate, InvitationCodeOut

router = APIRouter(prefix="/codes", tags=["invitation-codes"])
oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/token")


def _is_family_head(user_id: str, family_id: str) -> bool:
    r = (
        supabase.table("family_groups")
        .select("family_head_id")
        .eq("family_id", family_id)
        .single()
        .execute()
    )
    data = getattr(r, "data", None)
    return bool(data and data.get("family_head_id") == user_id)


def _generate_code_like(prefix: Optional[str] = None) -> str:
    # Fallback generator if client doesn't provide a code.
    part1 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    part2 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    if prefix:
        return f"{prefix}-{part1}-{part2}"
    return f"{part1}-{part2}"


@router.post("/generate", response_model=InvitationCodeOut)
def generate_code(payload: InvitationCodeCreate, token: str = Depends(oauth2)):
    user_id = get_user_id_from_token(token)

    # Authorization by target_type
    if payload.target_type == "classroom":
        # Teacher can only generate for their own user_id
        if str(payload.target_id) != user_id:
            raise HTTPException(status_code=403, detail="Not the owning teacher")
    elif payload.target_type == "family":
        if not _is_family_head(user_id, str(payload.target_id)):
            raise HTTPException(status_code=403, detail="Not family head for target family")
    else:
        raise HTTPException(status_code=400, detail="Invalid target_type")

    # Use provided code or generate one
    code_value = payload.code or _generate_code_like(
        "MATH" if payload.target_type == "classroom" else "FAM"
    )

    # Validate expires_at format if provided
    expires_at_iso = None
    if payload.expires_at is not None:
        # Ensure timezone-aware UTC ISO for storage consistency
        if isinstance(payload.expires_at, datetime):
            dt = payload.expires_at
        else:
            raise HTTPException(status_code=400, detail="expires_at must be ISO datetime")
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        expires_at_iso = dt.isoformat()

    # Insert
    ins = (
        supabase.table("invitation_codes")
        .insert({
            "code": code_value,
            "target_type": payload.target_type,
            "target_id": str(payload.target_id),
            "created_by": user_id,
            "expires_at": expires_at_iso,
            "max_uses": payload.max_uses,
        })
        .execute()
    )
    data = getattr(ins, "data", None)
    if not data:
        raise HTTPException(status_code=400, detail="Failed to create invitation code")
    row = data[0]
    # Derive status for newly created code (uses = 0)
    status = "active"
    exp_iso = row.get("expires_at")
    if exp_iso:
        try:
            exp_dt = datetime.fromisoformat(exp_iso.replace('Z', '+00:00'))
            if exp_dt.tzinfo is None:
                exp_dt = exp_dt.replace(tzinfo=timezone.utc)
            if datetime.now(timezone.utc) >= exp_dt:
                status = "expired"
        except Exception:
            pass
    if row.get("max_uses") is not None and row.get("max_uses") <= 0:
        status = "exhausted"

    return {
        "code_id": row["code_id"],
        "code": row["code"],
        "target_type": row["target_type"],
        "target_id": row["target_id"],
        "created_by": row["created_by"],
        "expires_at": row.get("expires_at"),
        "max_uses": row.get("max_uses"),
        "created_at": row.get("created_at"),
        "status": status,
    }


@router.get("/my")
def list_my_codes(
    token: str = Depends(oauth2),
    target_type: Optional[str] = None,
    active: Optional[bool] = None,
) -> Any:
    user_id = get_user_id_from_token(token)

    q = supabase.table("invitation_codes").select("*").eq("created_by", user_id)
    if target_type:
        q = q.eq("target_type", target_type)
    res = q.execute()
    codes = getattr(res, "data", []) or []

    # Attach usage counts from join_requests
    code_ids = [c["code_id"] for c in codes]
    usage_map: Dict[str, int] = {}
    if code_ids:
        reqs = (
            supabase.table("join_requests")
            .select("code_id")
            .in_("code_id", code_ids)
            .execute()
        )
        for row in getattr(reqs, "data", []) or []:
            cid = row.get("code_id")
            if cid:
                usage_map[cid] = usage_map.get(cid, 0) + 1

    # Compute derived fields: uses and status (active/expired/exhausted)
    now = datetime.now(timezone.utc)
    enriched: list[Dict[str, Any]] = []
    for c in codes:
        uses = usage_map.get(c["code_id"], 0)
        c["usage_count"] = uses
        c["uses"] = uses

        # Parse expires_at if present and determine expiry
        expires_at = c.get("expires_at")
        is_expired = False
        if expires_at:
            try:
                # Normalize 'Z' suffix to '+00:00' for fromisoformat
                exp_dt = datetime.fromisoformat(expires_at.replace('Z', '+00:00'))
                if exp_dt.tzinfo is None:
                    exp_dt = exp_dt.replace(tzinfo=timezone.utc)
                is_expired = now >= exp_dt
            except Exception:
                # If unparsable, do not mark as expired by parser error
                is_expired = False

        max_uses = c.get("max_uses")
        is_exhausted = isinstance(max_uses, int) and uses >= max_uses if max_uses is not None else False

        status = "active"
        if is_expired:
            status = "expired"
        elif is_exhausted:
            status = "exhausted"
        c["status"] = status

        # Optional filtering by active flag
        if active is None:
            enriched.append(c)
        elif active and status == "active":
            enriched.append(c)
        elif (active is False) and status != "active":
            enriched.append(c)

    return enriched


@router.get("/active")
def list_active_codes(token: str = Depends(oauth2)) -> Dict[str, Any]:
    """Return only active invitations wrapped as { invitations: [...] }.

    This is a thin wrapper over list_my_codes with active filtering and response
    shape aligned to the spec's active invitations endpoint.
    """
    # Reuse computation by calling the same query path
    user_id = get_user_id_from_token(token)
    # Fetch all and filter via active flag using the same logic as list_my_codes
    q = supabase.table("invitation_codes").select("*").eq("created_by", user_id)
    res = q.execute()
    codes = getattr(res, "data", []) or []

    # Build usage map
    code_ids = [c["code_id"] for c in codes]
    usage_map: Dict[str, int] = {}
    if code_ids:
        reqs = (
            supabase.table("join_requests").select("code_id").in_("code_id", code_ids).execute()
        )
        for row in getattr(reqs, "data", []) or []:
            cid = row.get("code_id")
            if cid:
                usage_map[cid] = usage_map.get(cid, 0) + 1

    # Enrich and keep only active
    now = datetime.now(timezone.utc)
    invitations: list[Dict[str, Any]] = []
    for c in codes:
        uses = usage_map.get(c["code_id"], 0)
        expires_at = c.get("expires_at")
        is_expired = False
        if expires_at:
            try:
                exp_dt = datetime.fromisoformat(expires_at.replace('Z', '+00:00'))
                if exp_dt.tzinfo is None:
                    exp_dt = exp_dt.replace(tzinfo=timezone.utc)
                is_expired = now >= exp_dt
            except Exception:
                is_expired = False
        max_uses = c.get("max_uses")
        is_exhausted = isinstance(max_uses, int) and uses >= max_uses if max_uses is not None else False

        status = "active"
        if is_expired:
            status = "expired"
        elif is_exhausted:
            status = "exhausted"

        if status == "active":
            invitations.append({
                **c,
                "uses": uses,
                "status": status,
            })

    return {"invitations": invitations}


@router.delete("/{code_id}")
def revoke_code(code_id: UUID, token: str = Depends(oauth2)) -> Dict[str, Any]:
    """Revoke an invitation code you created by making it immediately unusable.

    We do not delete the row to preserve history. Instead:
    - sets expires_at to now (UTC)
    - sets max_uses to current uses (so status becomes exhausted/expired)
    """
    user_id = get_user_id_from_token(token)

    # Fetch the code and verify ownership
    res = (
        supabase.table("invitation_codes")
        .select("*")
        .eq("code_id", str(code_id))
        .single()
        .execute()
    )
    code = getattr(res, "data", None)
    if not code:
        raise HTTPException(status_code=404, detail="Code not found")
    if code.get("created_by") != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to revoke this code")

    # Compute current uses
    usage = (
        supabase.table("join_requests")
        .select("count(*)", count="exact")
        .eq("code_id", str(code_id))
        .execute()
    )
    uses = 0
    try:
        uses = int(usage.data[0]["count"]) if usage and usage.data else 0
    except Exception:
        uses = 0

    now_iso = datetime.now(timezone.utc).isoformat()

    # Ensure max_uses is set to at least the current uses so it can't be used again
    current_max = code.get("max_uses")
    new_max = uses if current_max is None else max(uses, current_max)

    upd = (
        supabase.table("invitation_codes")
        .update({
            "expires_at": now_iso,
            "max_uses": new_max,
        })
        .eq("code_id", str(code_id))
        .execute()
    )
    updated = getattr(upd, "data", None)
    if not updated:
        raise HTTPException(status_code=400, detail="Failed to revoke code")
    return updated[0]


@router.delete("/{code_id}/revoke", status_code=204)
def revoke_code_no_content(code_id: UUID, token: str = Depends(oauth2)) -> Response:
    """No-content variant revoke to align with spec expectations (204).

    Internally reuses the same logic as revoke_code by performing the same
    updates, then returning 204.
    """
    # Perform the same checks and updates as revoke_code
    _ = revoke_code(code_id, token)
    return Response(status_code=204)
