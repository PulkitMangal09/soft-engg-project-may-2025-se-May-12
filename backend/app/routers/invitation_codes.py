# app/routers/invitation_codes.py
from fastapi import APIRouter, Depends, Header, HTTPException, Query, status
from typing import Optional, List
from uuid import UUID
import secrets, string
from postgrest import APIError

from ..config import supabase
from ..models import InvitationCodeCreate, InvitationCodeOut
from ..utils.profile_utils import get_user_id_from_token  # adjust import path if needed

router = APIRouter(prefix="/codes", tags=["Invitation Codes"])

# ---------- helpers ----------

def _require_token(authorization: Optional[str]) -> str:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
    return authorization.split(" ", 1)[1]

def _generate_unique_code(length: int = 8) -> str:
    alphabet = string.ascii_uppercase + string.digits
    for _ in range(10):
        candidate = "".join(secrets.choice(alphabet) for _ in range(length))
        try:
            resp = supabase.table("invitation_codes").select("code").eq("code", candidate).single().execute()
            if not getattr(resp, "data", None):  # not found -> unique
                return candidate
        except Exception:
            # .single() raises if not found; treat as unique
            return candidate
    # Fallback (extremely unlikely)
    return "".join(secrets.choice(alphabet) for _ in range(length + 2))

def _assert_teacher_owns_classroom(teacher_id: str, classroom_id: UUID):
    resp = supabase.table("classrooms").select("classroom_id, teacher_id").eq("classroom_id", str(classroom_id)).single().execute()
    data = getattr(resp, "data", None)
    if not data:
        raise HTTPException(status_code=404, detail="Classroom not found")
    if data["teacher_id"] != teacher_id:
        raise HTTPException(status_code=403, detail="You do not own this classroom")

def _append_usage_counts(codes: List[dict]) -> List[dict]:
    if not codes:
        return codes
    code_ids = [c["code_id"] for c in codes if "code_id" in c]
    if not code_ids:
        return codes
    try:
        jr = supabase.table("join_requests").select("code_id").in_("code_id", code_ids).execute()
        rows = getattr(jr, "data", []) or []
        counts = {}
        for r in rows:
            cid = r.get("code_id")
            if cid:
                counts[cid] = counts.get(cid, 0) + 1
        for c in codes:
            c["usage_count"] = counts.get(c.get("code_id"), 0)
    except Exception:
        for c in codes:
            c["usage_count"] = 0
    return codes

# ---------- routes ----------

@router.post(
    "",
    response_model=InvitationCodeOut,
    status_code=status.HTTP_201_CREATED,
    summary="Generate an invitation code",
)
def create_code(
    payload: InvitationCodeCreate,
    authorization: Optional[str] = Header(None),
):
    """
    Create an invitation code for a target (e.g., classroom).
    Works for both **Student** and **Parent** invites. The role is handled at redemption time.
    """
    token = _require_token(authorization)
    user_id = get_user_id_from_token(token)

    if payload.target_type == "classroom":
        _assert_teacher_owns_classroom(user_id, payload.target_id)

    # Ensure code uniqueness
    code_value = payload.code or _generate_unique_code()

    # IMPORTANT: serialize datetime to ISO string (httpx can't JSON-encode datetimes)
    expires_at_str = payload.expires_at.isoformat() if payload.expires_at else None

    insert_payload = {
        "code": code_value,
        "target_type": payload.target_type,
        "target_id": str(payload.target_id),
        "created_by": user_id,
        "expires_at": expires_at_str,      # serialized
        "max_uses": payload.max_uses,      # int or None
    }

    try:
        resp = supabase.table("invitation_codes").insert(insert_payload).execute()
    except APIError as e:
        raise HTTPException(status_code=400, detail=str(e))

    data = (getattr(resp, "data", None) or [None])[0]
    if not data:
        raise HTTPException(status_code=400, detail="Failed to create invitation code")

    return {
        "code_id": data["code_id"],
        "code": data["code"],
        "target_type": data["target_type"],
        "target_id": UUID(data["target_id"]),
        "created_by": UUID(data["created_by"]),
        "expires_at": data.get("expires_at"),
        "max_uses": data.get("max_uses"),
        "created_at": data.get("created_at"),
    }


@router.get("/my", summary="List invitation codes created by me")
def list_my_codes(
    authorization: Optional[str] = Header(None),
    target_type: Optional[str] = Query(None, description="Filter by target_type, e.g. 'classroom' or 'family'"),
):
    token = _require_token(authorization)
    user_id = get_user_id_from_token(token)

    q = supabase.table("invitation_codes").select("*").eq("created_by", user_id)
    if target_type:
        q = q.eq("target_type", target_type)

    resp = q.order("created_at", desc=True).execute()
    codes = getattr(resp, "data", []) or []
    codes = _append_usage_counts(codes)
    return codes


@router.get("/{code}", summary="Lookup an invitation code")
def get_code(code: str):
    try:
        resp = supabase.table("invitation_codes").select("*").eq("code", code).single().execute()
        data = getattr(resp, "data", None)
    except Exception:
        data = None
    if not data:
        raise HTTPException(status_code=404, detail="Code not found")
    return data


@router.delete("/{code_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Revoke (delete) an invitation code I created")
def delete_code(
    code_id: UUID,
    authorization: Optional[str] = Header(None),
):
    token = _require_token(authorization)
    user_id = get_user_id_from_token(token)

    resp = supabase.table("invitation_codes").select("created_by").eq("code_id", str(code_id)).single().execute()
    data = getattr(resp, "data", None)
    if not data:
        raise HTTPException(status_code=404, detail="Code not found")
    if data["created_by"] != user_id:
        raise HTTPException(status_code=403, detail="You can only delete your own codes")

    supabase.table("invitation_codes").delete().eq("code_id", str(code_id)).execute()
    return None
