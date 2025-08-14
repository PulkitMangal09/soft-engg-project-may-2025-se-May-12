from fastapi import APIRouter, HTTPException, Depends, Path, Body
from fastapi.security import OAuth2PasswordBearer
from typing import List, Dict, Any,Optional
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

    # --- generate a short, human-friendly key required by schema ---
    import random, string, time
    def _rand_key(n=8):
        # upper + digits, avoids easily-confused chars
        alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
        return "".join(random.choice(alphabet) for _ in range(n))

    # Try insert (retry once if key collides on unique index)
    attempt = 0
    while attempt < 2:
        attempt += 1
        family_key = _rand_key(8)

        payload = {
            "family_name": name,
            "family_key": family_key,          # <- REQUIRED
            "family_head_id": user_id,
            "description": description,
            "is_active": True,
        }

        ins = supabase.table("family_groups").insert(payload).execute()
        if getattr(ins, "data", None):
            group = ins.data[0]
            break

        # If there’s a unique violation on family_key, try again once
        err = getattr(ins, "error", None)
        if not err or getattr(err, "code", "") != "23505":
            raise HTTPException(400, detail="Could not create family group")

        time.sleep(0.05)  # tiny backoff and retry
    else:
        raise HTTPException(400, detail="Could not create family group (key collision)")

    # Create a reusable family invitation code (optional; keep your existing logic)
    try:
        from random import choices
        import string as _string
        part1 = ''.join(choices(_string.ascii_uppercase + _string.digits, k=6))
        part2 = ''.join(choices(_string.ascii_uppercase + _string.digits, k=6))
        fam_code = f"FAM-{part1}-{part2}"

        code_ins = (
            supabase.table("invitation_codes")
            .insert({
                "code": fam_code,
                "target_type": "family",
                "target_id": group["family_id"],
                "created_by": user_id,
                "max_uses": None,
                "expires_at": None,
            })
            .execute()
        )
        if getattr(code_ins, "data", None):
            group["family_code"] = fam_code
    except Exception:
        pass

    return group



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
    # Enrich members with user profile fields (full_name/name/email)
    members = members or []
    try:
        user_ids = [m["user_id"] for m in members] if members else []
        if user_ids:
            users_res = (
                supabase
                .table("users")
                .select("user_id, full_name, email, user_type")
                .in_("user_id", user_ids)
                .execute()
            )
            users = getattr(users_res, "data", None) or []
            by_id = {u["user_id"]: u for u in users}
            for m in members:
                u = by_id.get(m["user_id"]) or {}
                # copy common fields; keep keys consistent with frontend expectations
                if "full_name" in u and u["full_name"]:
                    m["full_name"] = u["full_name"]
                if "email" in u and u["email"]:
                    m["email"] = u["email"]
                # derive display role: keep 'head' if set; else from user_type
                try:
                    if m.get("role") == "head":
                        m["display_role"] = "head"
                    else:
                        utype = u.get("user_type")
                        if utype in ("parent", "teacher"):
                            m["display_role"] = utype
                        else:
                            m["display_role"] = "child"
                except Exception:
                    pass
    except Exception:
        # If enrichment fails, proceed with base member info
        pass

    grp["members"] = members
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


@router.post("/join")
def join_family_via_code(
    family_code: str = Body(..., embed=True),
    role: str = Body("relative", embed=True),
    message: str = Body(None, embed=True),
    token: str = Depends(oauth2),
) -> Dict[str, Any]:
    """Join a family by providing a family_code. Creates a pending join request.

    Implementation uses the same mechanism as invitation code redeem.
    """
    user_id = get_user_id(token)

    # Lookup invitation code by code value
    code_res = (
        supabase.table("invitation_codes")
        .select("*")
        .eq("code", family_code)
        .single()
        .execute()
    )
    code = getattr(code_res, "data", None)
    if not code or code.get("target_type") != "family":
        raise HTTPException(status_code=404, detail="Family code not found")

    # Validate expiry and uses similar to redeem
    exp = code.get("expires_at")
    if exp:
        try:
            from datetime import datetime, timezone as _tz
            exp_dt = datetime.fromisoformat(exp.replace('Z', '+00:00'))
            if exp_dt.tzinfo is None:
                exp_dt = exp_dt.replace(tzinfo=_tz.utc)
            if datetime.now(_tz.utc) >= exp_dt:
                raise HTTPException(status_code=400, detail="Family code expired")
        except HTTPException:
            raise
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid family code expiry format")

    max_uses = code.get("max_uses")
    if isinstance(max_uses, int):
        used = (
            supabase.table("join_requests")
            .select("code_id")
            .eq("code_id", code["code_id"])
            .execute()
        )
        used_count = len(getattr(used, "data", []) or [])
        if used_count >= max_uses:
            raise HTTPException(status_code=400, detail="Family code usage limit reached")

    # Create pending join request
    ins = (
        supabase.table("join_requests")
        .insert({
            "requester_id": user_id,
            "target_type": "family",
            "target_id": code["target_id"],
            "relationship_type": role,
            "message": message,
            "status": "pending",
            "code_id": code["code_id"],
        })
        .execute()
    )
    data = getattr(ins, "data", None)
    if not data:
        raise HTTPException(status_code=400, detail="Failed to create join request")
    return data[0]
@router.patch("/groups/{group_id}", response_model=Dict[str, Any])
def update_family_group(
    group_id: UUID = Path(...),
    name: Optional[str] = Body(None, embed=True),
    description: Optional[str] = Body(None, embed=True),
    token: str = Depends(oauth2),
):
    """Edit a family group you head (name/description)."""
    user_id = get_user_id(token)

    # ensure head
    grp = (
        supabase.table("family_groups")
        .select("family_head_id")
        .eq("family_id", str(group_id))
        .single()
        .execute()
        .data
    )
    if not grp or grp["family_head_id"] != user_id:
        raise HTTPException(403, "Not authorized to edit this family")

    payload = {}
    if name is not None:
        payload["family_name"] = name
    if description is not None:
        payload["description"] = description
    if not payload:
        raise HTTPException(400, "Nothing to update")

    upd = (
        supabase.table("family_groups")
        .update(payload)
        .eq("family_id", str(group_id))
        .execute()
    )
    if not upd.data:
        raise HTTPException(400, "Update failed")
    return upd.data[0]


@router.delete("/groups/{group_id}", response_model=Dict[str, Any])
def delete_family_group(
    group_id: UUID = Path(...),
    token: str = Depends(oauth2),
):
    """Delete a family group you head. (Soft delete is recommended; here we hard-delete + related.)"""
    user_id = get_user_id(token)

    grp = (
        supabase.table("family_groups")
        .select("family_head_id")
        .eq("family_id", str(group_id))
        .single()
        .execute()
        .data
    )
    if not grp or grp["family_head_id"] != user_id:
        raise HTTPException(403, "Not authorized to delete this family")

    # clean up related rows (best if you have FK ON DELETE CASCADE instead)
    supabase.table("family_members").delete().eq("family_id", str(group_id)).execute()
    supabase.table("join_requests").delete().eq("target_type", "family").eq("target_id", str(group_id)).execute()
    supabase.table("invitation_codes").delete().eq("target_type", "family").eq("target_id", str(group_id)).execute()

    supabase.table("family_groups").delete().eq("family_id", str(group_id)).execute()
    return {"deleted": True}

@router.get("/memberships")
def list_my_family_memberships(token: str = Depends(oauth2)):
    """Groups where the current user is a member (not necessarily head)."""
    user_id = get_user_id(token)

    members = (
        supabase.table("family_members")
        .select("family_id, role, joined_at")
        .eq("user_id", str(user_id))
        .execute()
        .data or []
    )
    if not members:
        return []

    family_ids = [m["family_id"] for m in members]
    groups = (
        supabase.table("family_groups")
        .select("family_id, family_name, family_head_id, created_at")
        .in_("family_id", family_ids)
        .execute()
        .data or []
    )

    # head name (optional)
    head_ids = list({g["family_head_id"] for g in groups})
    heads = {}
    if head_ids:
      res = supabase.table("users").select("user_id, full_name").in_("user_id", head_ids).execute()
      for r in res.data or []:
        heads[r["user_id"]] = r.get("full_name") or "Family Head"

    # merge
    out = []
    by_id = {m["family_id"]: m for m in members}
    for g in groups:
        m = by_id.get(g["family_id"], {})
        out.append({
            "family_id": g["family_id"],
            "family_name": g["family_name"],
            "role": m.get("role"),
            "joined_at": m.get("joined_at"),
            "member_count": None,  # optional: compute via count if needed
            "head_name": heads.get(g["family_head_id"]),
        })
    return out

@router.post("/classrooms/join")
def join_classroom_via_code(
    invite_code: str = Body(..., embed=True),
    relationship_type: str = Body("parent_student", embed=True),
    message: str = Body(None, embed=True),
    token: str = Depends(oauth2),
):
    """
    Parent (or teacher) joins a classroom using an invite code.
    Creates a pending join request that teachers can accept from their MyStudentsView.
    """
    user_id = get_user_id(token)

    code_res = (
        supabase.table("invitation_codes")
        .select("*")
        .eq("code", invite_code)
        .single()
        .execute()
    )
    code = getattr(code_res, "data", None)
    if not code:
        raise HTTPException(status_code=404, detail="Invite code not found")

    # Accept teacher/parent classroom codes
    if code.get("target_type") not in ("teacher_student", "parent_student"):
        raise HTTPException(status_code=400, detail="This code is not a classroom invite")

    # expiry / usage checks (like family join)
    exp = code.get("expires_at")
    if exp:
        from datetime import datetime, timezone as _tz
        exp_dt = datetime.fromisoformat(exp.replace('Z', '+00:00'))
        if exp_dt.tzinfo is None:
            exp_dt = exp_dt.replace(tzinfo=_tz.utc)
        if datetime.now(_tz.utc) >= exp_dt:
            raise HTTPException(status_code=400, detail="Invite code expired")

    max_uses = code.get("max_uses")
    if isinstance(max_uses, int):
        used = (
            supabase.table("join_requests")
            .select("code_id")
            .eq("code_id", code["code_id"])
            .execute()
        )
        if len(getattr(used, "data", []) or []) >= max_uses:
            raise HTTPException(status_code=400, detail="Invite code usage limit reached")

    ins = (
        supabase.table("join_requests")
        .insert({
            "requester_id": str(user_id),
            "requester_type": "parent",               # or 'teacher' if needed
            "target_type": "classroom",
            "target_id": code["target_id"],           # classroom_id
            "relationship_type": relationship_type,   # 'parent_student'
            "message": message,
            "status": "pending",
            "code_id": code["code_id"],
        })
        .execute()
    )
    data = getattr(ins, "data", None)
    if not data:
        raise HTTPException(status_code=400, detail="Failed to create join request")
    return data[0]
