from fastapi import APIRouter, HTTPException, Depends, Path
from fastapi.security import OAuth2PasswordBearer
from typing import Any, Dict, Optional, List
from uuid import UUID
from datetime import datetime, timezone

from ..config import supabase
from ..utils.profile_utils import get_user_id_from_token, get_user_type
from ..models import CodeRedeemRequest

router = APIRouter(prefix="/requests", tags=["connection-requests"])
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


def _get_code_row(code: str) -> Optional[Dict[str, Any]]:
    res = (
        supabase.table("invitation_codes")
        .select("*")
        .eq("code", code)
        .single()
        .execute()
    )
    return getattr(res, "data", None)


def _get_code_usage_count(code_id: str) -> int:
    res = (
        supabase.table("join_requests")
        .select("code_id")
        .eq("code_id", code_id)
        .execute()
    )
    rows = getattr(res, "data", []) or []
    return len(rows)


@router.post("/redeem")
def redeem_code(payload: CodeRedeemRequest, token: str = Depends(oauth2)) -> Dict[str, Any]:
    user_id = get_user_id_from_token(token)

    code_row = _get_code_row(payload.code)
    if not code_row:
        raise HTTPException(status_code=404, detail="Code not found")

    # Validate expiry
    expires_at = code_row.get("expires_at")
    if expires_at:
        try:
            # Supabase returns ISO strings; compare with now
            exp_dt = datetime.fromisoformat(expires_at.replace("Z", "+00:00"))
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid code expiry format")
        if datetime.now(timezone.utc) >= exp_dt.astimezone(timezone.utc):
            raise HTTPException(status_code=400, detail="Code expired")

    # Validate max_uses (count all requests created with this code)
    max_uses = code_row.get("max_uses")
    if isinstance(max_uses, int):
        used = _get_code_usage_count(code_row["code_id"])  # pending+approved
        if used >= max_uses:
            raise HTTPException(status_code=400, detail="Code usage limit reached")

    # Create pending join request
    ins = (
        supabase.table("join_requests")
        .insert({
            "requester_id": user_id,
            "target_type": code_row["target_type"],  # 'family' | 'classroom'
            "target_id": code_row["target_id"],
            "relationship_type": payload.relationship_type,
            "message": payload.message,
            "status": "pending",
            "code_id": code_row["code_id"],
        })
        .execute()
    )
    data = getattr(ins, "data", None)
    if not data:
        raise HTTPException(status_code=400, detail="Failed to create request")
    return data[0]


@router.get("/pending")
def list_pending_requests(token: str = Depends(oauth2)) -> List[Dict[str, Any]]:
    user_id = get_user_id_from_token(token)

    pending: List[Dict[str, Any]] = []

    # Family: families where I'm head
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
        pending.extend(fam_reqs)

    # Classroom: if I'm a teacher, requests targeting my user_id
    user_type = get_user_type(user_id)
    if user_type == "teacher":
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
        pending.extend(t_reqs)

    return pending


@router.post("/{request_id}/approve")
def approve_request(request_id: UUID = Path(...), token: str = Depends(oauth2)) -> Dict[str, Any]:
    user_id = get_user_id_from_token(token)

    req_res = (
        supabase.table("join_requests").select("*").eq("request_id", str(request_id)).single().execute()
    )
    req = getattr(req_res, "data", None)
    if not req or req.get("status") != "pending":
        raise HTTPException(status_code=404, detail="Pending request not found")

    target_type = req["target_type"]
    target_id = req["target_id"]

    # Authorization check
    if target_type == "family":
        if not _is_family_head(user_id, target_id):
            raise HTTPException(status_code=403, detail="Not family head")
    elif target_type == "classroom":
        if target_id != user_id:
            raise HTTPException(status_code=403, detail="Not the owning teacher")
    else:
        raise HTTPException(status_code=400, detail="Invalid target_type")

    # Mark approved
    supabase.table("join_requests").update({
        "status": "approved",
        "responded_at": datetime.now(timezone.utc).isoformat(),
        "responded_by": user_id,
    }).eq("request_id", str(request_id)).execute()

    # Family: ensure membership exists (DB trigger handles user_connections)
    if target_type == "family":
        # Insert into family_members if missing
        exists = (
            supabase.table("family_members")
            .select("member_id")
            .eq("family_id", target_id)
            .eq("user_id", req["requester_id"])
            .execute()
            .data
        )
        if not exists:
            supabase.table("family_members").insert({
                "family_id": target_id,
                "user_id": req["requester_id"],
                "role": req.get("relationship_type"),
            }).execute()

    return {"request_id": str(request_id), "status": "approved"}


@router.post("/{request_id}/reject")
def reject_request(request_id: UUID = Path(...), token: str = Depends(oauth2)) -> Dict[str, Any]:
    user_id = get_user_id_from_token(token)

    req_res = (
        supabase.table("join_requests").select("*").eq("request_id", str(request_id)).single().execute()
    )
    req = getattr(req_res, "data", None)
    if not req or req.get("status") != "pending":
        raise HTTPException(status_code=404, detail="Pending request not found")

    target_type = req["target_type"]
    target_id = req["target_id"]

    # Authorization check
    if target_type == "family":
        if not _is_family_head(user_id, target_id):
            raise HTTPException(status_code=403, detail="Not family head")
    elif target_type == "classroom":
        if target_id != user_id:
            raise HTTPException(status_code=403, detail="Not the owning teacher")
    else:
        raise HTTPException(status_code=400, detail="Invalid target_type")

    supabase.table("join_requests").update({
        "status": "rejected",
        "responded_at": datetime.now(timezone.utc).isoformat(),
        "responded_by": user_id,
    }).eq("request_id", str(request_id)).execute()

    return {"request_id": str(request_id), "status": "rejected"}


# --- Spec-aligned wrapper endpoints (Phase 1) ---

@router.post("/request")
def create_request_alias(payload: Dict[str, Any], token: str = Depends(oauth2)) -> Dict[str, Any]:
    """Alias for sending a connection request using an invitation code.

    Expected payload keys (spec):
      - invitation_code: str
      - message: Optional[str]
      - relationship: str
    """
    body_code = payload.get("invitation_code")
    relationship = payload.get("relationship")
    message = payload.get("message")
    if not body_code or not relationship:
        raise HTTPException(status_code=422, detail="invitation_code and relationship are required")

    model = CodeRedeemRequest(code=body_code, relationship_type=relationship, message=message)
    created = redeem_code(model, token)
    return {
        "request_id": created.get("request_id"),
        "status": created.get("status", "pending"),
        "message": "Request sent successfully",
    }


@router.get("/pending-requests")
def list_my_pending_requests(token: str = Depends(oauth2)) -> List[Dict[str, Any]]:
    """List the caller's own pending outbound requests."""
    user_id = get_user_id_from_token(token)

    q = (
        supabase.table("join_requests")
        .select("*")
        .eq("requester_id", user_id)
        .eq("status", "pending")
    )

    # Try to order by created_at if it exists; otherwise fall back with no ordering.
    try:
        rows = q.order("created_at", desc=True).execute()
    except Exception:
        rows = q.execute()

    data = getattr(rows, "data", []) or []
    return data



@router.patch("/{request_id}/handle")
def handle_request(request_id: UUID = Path(...), payload: Dict[str, Any] = None, token: str = Depends(oauth2)) -> Dict[str, Any]:
    """Unified handler to accept/reject a request.

    Payload: { action: "accept" | "reject", message?: str }
    """
    action = (payload or {}).get("action")
    if action not in ("accept", "reject"):
        raise HTTPException(status_code=422, detail="action must be 'accept' or 'reject'")

    # Perform action
    if action == "accept":
        _ = approve_request(request_id, token)
        status = "accepted"
        # Best-effort: find a resulting connection between approver and requester
        # Load request to know requester
        req_res = (
            supabase.table("join_requests").select("*").eq("request_id", str(request_id)).single().execute()
        )
        req = getattr(req_res, "data", None)
        connection_id = None
        if req:
            approver_id = get_user_id_from_token(token)
            requester_id = req.get("requester_id")
            # Search latest connection linking these two users
            conn_res = (
                supabase.table("user_connections")
                .select("*")
                .or_(f"and(user_id_1.eq.{approver_id},user_id_2.eq.{requester_id}),and(user_id_2.eq.{approver_id},user_id_1.eq.{requester_id})")
                .order("established_at", desc=True)
                .limit(1)
                .execute()
            )
            rows = getattr(conn_res, "data", []) or []
            if rows:
                connection_id = rows[0].get("connection_id")
        return {"status": status, "connection_id": connection_id}
    else:
        _ = reject_request(request_id, token)
        return {"status": "rejected"}
