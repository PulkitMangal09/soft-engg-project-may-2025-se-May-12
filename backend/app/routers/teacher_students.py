# app/routers/teacher_students.py
from fastapi import APIRouter, Depends, Header, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Literal
from uuid import UUID
import secrets, string, datetime
import datetime

from postgrest import APIError
from ..config import supabase

router = APIRouter(prefix="/teacher", tags=["Teacher • Students & Classrooms"])

# ---------------- Auth helpers ----------------
def _get_bearer_token(authorization: str = Header(...)) -> str:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
    return authorization.split(" ", 1)[1].strip()

def _get_user_id_from_token(token: str) -> str:
    auth_res = supabase.auth.get_user(token)
    if getattr(auth_res, "error", None):
        raise HTTPException(status_code=401, detail="Unauthorized")
    return auth_res.user.id

# ---------------- Schemas ----------------
class ClassroomCreate(BaseModel):
    name: str = Field(..., description="Classroom name")
    subject: str
    school_name: Optional[str] = None
    grade_level: Optional[str] = None
    max_students: Optional[int] = Field(None, ge=1)

class ClassroomUpdate(BaseModel):
    name: Optional[str] = None
    subject: Optional[str] = None
    school_name: Optional[str] = None
    grade_level: Optional[str] = None
    max_students: Optional[int] = Field(None, ge=1)
    is_active: Optional[bool] = None

class RequestRespond(BaseModel):
    action: Literal["accepted", "rejected"]

# ---------------- Internals ----------------
def _rand_key(n: int = 6) -> str:
    alphabet = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(n))

def _create_payload(body: ClassroomCreate, teacher_id: str) -> Dict[str, Any]:
    return {
        "classroom_name": body.name,
        "classroom_key": _rand_key(8),
        "teacher_id": teacher_id,
        "subject": body.subject,
        "grade_level": body.grade_level,
        "school_name": body.school_name,
        "max_students": body.max_students or 30,
        "is_active": True,
    }

def _update_payload(body: ClassroomUpdate) -> Dict[str, Any]:
    raw = {
        "classroom_name": body.name,
        "subject": body.subject,
        "grade_level": body.grade_level,
        "school_name": body.school_name,
        "max_students": body.max_students,
        "is_active": body.is_active,
    }
    return {k: v for k, v in raw.items() if v is not None}

def _fetch_classroom(classroom_id: str) -> Optional[Dict[str, Any]]:
    try:
        resp = (
            supabase.table("classrooms")
            .select(
                "classroom_id, classroom_name, classroom_key, subject, grade_level, "
                "school_name, max_students, is_active, created_at, teacher_id"
            )
            .eq("classroom_id", classroom_id)
            .limit(1)
            .execute()
        )
        data = getattr(resp, "data", None) or []
        return data[0] if data else None
    except APIError as e:
        raise HTTPException(status_code=400, detail=str(e))

def _assert_owner_or_404(classroom_id: str, teacher_id: str) -> Dict[str, Any]:
    row = _fetch_classroom(classroom_id)
    if not row:
        raise HTTPException(status_code=404, detail=f"Classroom {classroom_id} not found")
    if row["teacher_id"] != teacher_id:
        raise HTTPException(status_code=403, detail="Not your classroom")
    return row

def _normalize_row_for_ui(row: Dict[str, Any]) -> Dict[str, Any]:
    if row and "classroom_name" in row:
        row["name"] = row["classroom_name"]
    return row

def _teacher_classroom_ids(teacher_id: str) -> List[str]:
    rows = (
        supabase.table("classrooms")
        .select("classroom_id")
        .eq("teacher_id", teacher_id)
        .execute()
        .data or []
    )
    return [r["classroom_id"] for r in rows]

# ---------------- Classrooms ----------------

@router.get("/classrooms")
def list_classrooms(authorization: str = Header(...)):
    token = _get_bearer_token(authorization)
    teacher_id = _get_user_id_from_token(token)
    try:
        resp = (
            supabase.table("classrooms")
            .select(
                "classroom_id, classroom_name, classroom_key, subject, grade_level, "
                "school_name, max_students, is_active, created_at, teacher_id"
            )
            .eq("teacher_id", teacher_id)
            .order("created_at", desc=True)
            .execute()
        )
        rows = getattr(resp, "data", []) or []
        return [_normalize_row_for_ui(r) for r in rows]
    except APIError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/classrooms/{classroom_id}")
def get_classroom(classroom_id: UUID, authorization: str = Header(...)):
    token = _get_bearer_token(authorization)
    teacher_id = _get_user_id_from_token(token)
    row = _assert_owner_or_404(str(classroom_id), teacher_id)
    return _normalize_row_for_ui(row)

@router.post("/classrooms")
def create_classroom(body: ClassroomCreate, authorization: str = Header(...)):
    token = _get_bearer_token(authorization)
    teacher_id = _get_user_id_from_token(token)
    payload = _create_payload(body, teacher_id)

    # try to avoid duplicate classroom_key collisions
    for _ in range(5):
        try:
            supabase.table("classrooms").insert(payload).execute()
            # read back inserted row by (teacher_id, classroom_key)
            out = (
                supabase.table("classrooms")
                .select(
                    "classroom_id, classroom_name, classroom_key, subject, grade_level, "
                    "school_name, max_students, is_active, created_at, teacher_id"
                )
                .eq("teacher_id", teacher_id)
                .eq("classroom_key", payload["classroom_key"])
                .limit(1)
                .execute()
                .data
            ) or []
            if out:
                return _normalize_row_for_ui(out[0])
        except APIError as e:
            # regenerate key if unique violation
            if "classroom_key" in str(e).lower() and "duplicate" in str(e).lower():
                payload["classroom_key"] = _rand_key(8)
                continue
            raise HTTPException(status_code=422, detail=str(e))
    raise HTTPException(status_code=422, detail="Failed to generate unique classroom key")

@router.patch("/classrooms/{classroom_id}")
def update_classroom(classroom_id: UUID, body: ClassroomUpdate, authorization: str = Header(...)):
    token = _get_bearer_token(authorization)
    teacher_id = _get_user_id_from_token(token)
    _assert_owner_or_404(str(classroom_id), teacher_id)

    updates = _update_payload(body)
    if not updates:
        raise HTTPException(status_code=400, detail="No fields to update")
    try:
        supabase.table("classrooms") \
            .update(updates) \
            .eq("classroom_id", str(classroom_id)) \
            .eq("teacher_id", teacher_id) \
            .execute()
        updated = _fetch_classroom(str(classroom_id))
        if not updated:
            raise HTTPException(status_code=404, detail="Classroom not found after update")
        return _normalize_row_for_ui(updated)
    except APIError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/classrooms/{classroom_id}")
def delete_classroom(
    classroom_id: UUID,
    authorization: str = Header(...),
    hard: bool = Query(False, description="If true, hard delete; otherwise soft-delete"),
):
    token = _get_bearer_token(authorization)
    teacher_id = _get_user_id_from_token(token)
    _assert_owner_or_404(str(classroom_id), teacher_id)

    try:
        if hard:
            supabase.table("classroom_students").delete().eq("classroom_id", str(classroom_id)).execute()
            supabase.table("classrooms").delete().eq("classroom_id", str(classroom_id)).eq("teacher_id", teacher_id).execute()
            return {"ok": True, "deleted": str(classroom_id)}
        else:
            supabase.table("classrooms").update({"is_active": False}).eq("classroom_id", str(classroom_id)).eq("teacher_id", teacher_id).execute()
            row = _fetch_classroom(str(classroom_id))
            if not row:
                raise HTTPException(status_code=404, detail="Classroom not found for soft delete")
            return {"ok": True, "classroom_id": row["classroom_id"], "is_active": row["is_active"]}
    except APIError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/classrooms/{classroom_id}/students")
def list_classroom_students(classroom_id: UUID, authorization: str = Header(...)):
    token = _get_bearer_token(authorization)
    teacher_id = _get_user_id_from_token(token)
    _assert_owner_or_404(str(classroom_id), teacher_id)
    try:
        resp = (
            supabase.table("classroom_students")
            .select(
                "enrollment_id, enrolled_at, is_active, "
                "students:student_id (student_id, name, email, grade_level, school_name)"
            )
            .eq("classroom_id", str(classroom_id))
            .execute()
        )
        return getattr(resp, "data", []) or []
    except APIError as e:
        raise HTTPException(status_code=400, detail=str(e))

# ---------------- Metrics ----------------

@router.get("/students/metrics")
def students_metrics(authorization: str = Header(...)):
    token = _get_bearer_token(authorization)
    teacher_id = _get_user_id_from_token(token)

    cls = supabase.table("classrooms").select("classroom_id,is_active").eq("teacher_id", teacher_id).execute().data or []
    total_classrooms = len(cls)
    active_classrooms = sum(1 for c in cls if c.get("is_active", True))

    # total students (count distinct students across this teacher's classrooms)
    classroom_ids = [c["classroom_id"] for c in cls]
    total_students = 0
    if classroom_ids:
        rows = (
            supabase.table("classroom_students")
            .select("student_id")
            .in_("classroom_id", classroom_ids)
            .execute()
            .data or []
        )
        # distinct
        total_students = len({r["student_id"] for r in rows})

    # by grade (quick aggregate over all students table; could be refined to only students in teacher's classes)
    by: Dict[str, int] = {}
    for r in supabase.table("students").select("grade_level").execute().data or []:
        g = r.get("grade_level") or "N/A"
        by[g] = by.get(g, 0) + 1

    return {
        "total_classrooms": total_classrooms,
        "active_classrooms": active_classrooms,
        "total_students": total_students,
        "by_grade_level": by,
    }

# ---------------- Connection Requests ----------------

@router.get("/requests")
def list_requests(status: str = Query("pending"), authorization: str = Header(...)):
    """
    List join/connection requests that target this teacher's classrooms.
    """
    token = _get_bearer_token(authorization)
    teacher_id = _get_user_id_from_token(token)

    cls_ids = _teacher_classroom_ids(teacher_id)
    if not cls_ids:
        return []

    try:
        # Pull requests for these classrooms
        reqs = (
            supabase.table("join_requests")
            .select("request_id, requester_id, target_type, target_id, relationship_type, message, status, requested_at, created_at")
            .eq("target_type", "classroom")
            .in_("target_id", cls_ids)
            .eq("status", status)
            .order("requested_at", desc=True)
            .execute()
            .data or []
        )

        if not reqs:
            return []

        requester_ids = list({r["requester_id"] for r in reqs})
        users = (
            supabase.table("users")
            .select("user_id, full_name, email, user_type")
            .in_("user_id", requester_ids)
            .execute()
            .data or []
        )
        user_map = {u["user_id"]: u for u in users}

        classrooms = (
            supabase.table("classrooms")
            .select("classroom_id, classroom_name")
            .in_("classroom_id", list({r["target_id"] for r in reqs}))
            .execute()
            .data or []
        )
        cls_map = {c["classroom_id"]: c for c in classrooms}

        out = []
        for r in reqs:
            u = user_map.get(r["requester_id"], {})
            c = cls_map.get(r["target_id"], {})
            out.append({
                "request_id": r["request_id"],
                "requested_at": r.get("requested_at") or r.get("created_at"),
                "message": r.get("message") or "",
                "status": r.get("status"),
                "relationship_type": r.get("relationship_type"),
                "classroom_id": r["target_id"],
                "classroom_name": c.get("classroom_name"),
                "requester": {
                    "user_id": u.get("user_id"),
                    "full_name": u.get("full_name"),
                    "email": u.get("email"),
                    "user_type": u.get("user_type"),
                },
            })
        return out
    except APIError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/requests/{request_id}")
def respond_request(request_id: UUID, body: RequestRespond, authorization: str = Header(...)):
    """
    Accept or reject a request. On 'accepted':
      - if requester is student and target is classroom -> ensure students row exists, then idempotent enroll in classroom_students
      - if requester is parent -> idempotent user_connections add to teacher
    """
    token = _get_bearer_token(authorization)
    teacher_id = _get_user_id_from_token(token)

    # Load request
    req_rows = (
        supabase.table("join_requests")
        .select("*")
        .eq("request_id", str(request_id))
        .limit(1)
        .execute()
        .data or []
    )
    if not req_rows:
        raise HTTPException(status_code=404, detail="Request not found")
    req = req_rows[0]

    if req.get("status") != "pending":
        raise HTTPException(status_code=400, detail="Request already processed")

    if req.get("target_type") != "classroom":
        raise HTTPException(status_code=400, detail="Unsupported target type")

    # Ensure this classroom belongs to the teacher
    _assert_owner_or_404(req["target_id"], teacher_id)

    # Fetch requester user
    u_rows = (
        supabase.table("users")
        .select("user_id, user_type, full_name, email")
        .eq("user_id", req["requester_id"])
        .limit(1)
        .execute()
        .data or []
    )
    if not u_rows:
        raise HTTPException(status_code=404, detail="Requester user not found")
    requester_user = u_rows[0]
    requester_id = requester_user["user_id"]

    # If rejecting, just update status
    if body.action == "rejected":
        final = _set_request_status(str(request_id), teacher_id, "rejected")
        return {"ok": True, "request_id": str(request_id), "status": final}

    # Accepting: perform side-effects FIRST, then mark accepted.
    try:
        if requester_user.get("user_type") == "student":
            # ---- ensure students row exists ----
            st = (
                supabase.table("students")
                .select("student_id")
                .eq("student_id", requester_id)
                .limit(1)
                .execute()
                .data or []
            )
            if not st:
                # create minimal student row (email/name from users)
                supabase.table("students").insert({
                    "student_id": requester_id,
                    "email": requester_user.get("email"),
                    "name": requester_user.get("full_name"),
                }).execute()

            # ---- idempotent enrollment ----
            exists = (
                supabase.table("classroom_students")
                .select("enrollment_id")
                .eq("classroom_id", req["target_id"])
                .eq("student_id", requester_id)
                .limit(1)
                .execute()
                .data or []
            )
            if not exists:
                supabase.table("classroom_students").insert({
                    "classroom_id": req["target_id"],
                    "student_id": requester_id,
                    "is_active": True,
                }).execute()

        elif requester_user.get("user_type") == "parent":
            # ---- idempotent teacher<->parent connection ----
            conn_exists = (
                supabase.table("user_connections")
                .select("connection_id")
                .or_(f"user_id_1.eq.{teacher_id},user_id_2.eq.{teacher_id}")  # either side
                .or_(f"user_id_1.eq.{requester_id},user_id_2.eq.{requester_id}")
                .eq("connection_type", "teacher_parent")
                .execute()
                .data or []
            )
            # The above OR is a broad check; if you want exact pair check, do two eq filters:
            exact_exists = (
                supabase.table("user_connections")
                .select("connection_id")
                .eq("user_id_1", teacher_id).eq("user_id_2", requester_id)
                .eq("connection_type", "teacher_parent")
                .execute()
                .data or []
            ) or (
                supabase.table("user_connections")
                .select("connection_id")
                .eq("user_id_1", requester_id).eq("user_id_2", teacher_id)
                .eq("connection_type", "teacher_parent")
                .execute()
                .data or []
            )
            if not exact_exists:
                supabase.table("user_connections").insert({
                    "user_id_1": teacher_id,
                    "user_id_2": requester_id,
                    "connection_type": "teacher_parent",
                }).execute()
        else:
            raise HTTPException(status_code=400, detail="Unsupported requester user_type")
    except APIError as e:
        # Side-effect failed -> do NOT mark accepted; return error detail
        raise HTTPException(status_code=400, detail=str(e))

    final = _set_request_status(str(request_id), teacher_id, "accepted")
    return {"ok": True, "request_id": str(request_id), "status": final}

def _set_request_status(request_id: str, teacher_id: str, preferred: str) -> str:
    """Update join_requests.status trying compatible enum labels if needed."""
    # Map the label we *want* to what the DB might actually use
    candidates_map = {
        "accepted": ["accepted", "approved", "confirmed"],
        "rejected": ["rejected", "declined"],
        "pending":  ["pending"]
    }
    candidates = candidates_map.get(preferred, [preferred])

    last_err = None
    for st in candidates:
        try:
            supabase.table("join_requests").update({
                "status": st,
                "responded_at": datetime.datetime.utcnow().isoformat(),
                "responded_by": teacher_id,
            }).eq("request_id", request_id).execute()
            return st
        except APIError as e:
            # try the next candidate if it's an enum value issue, else rethrow
            msg = str(e)
            if "22P02" in msg and "invalid input value for enum" in msg:
                last_err = e
                continue
            raise
    # If we tried all candidates and failed, surface a clear error
    raise HTTPException(
        status_code=400,
        detail=f"Unsupported status in DB enum. Tried: {', '.join(candidates)}"
    )
