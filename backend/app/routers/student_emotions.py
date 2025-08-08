from fastapi import APIRouter, Depends, HTTPException, Body, UploadFile, File, Form
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer
from typing import List
from ..config import supabase
from ..models import (
    EmotionalEntry, MoodLog, ChatSession, ChatMessage, EmergencyContact, SenderTypeEnum
)
from ..routers import chat_bot as chat_bot_module
import json

router = APIRouter(prefix="/student/emotions", tags=["student-emotions"])
oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/token")


def get_user_id(token: str):
    auth_res = supabase.auth.get_user(token)
    if getattr(auth_res, 'error', None):
        raise HTTPException(status_code=401, detail="Unauthorized")
    return auth_res.user.id

# -------------------------------
# CRUD for emotional_entries
# -------------------------------


@router.post("/entries", response_model=EmotionalEntry)
def create_emotional_entry(entry: EmotionalEntry, token: str = Depends(oauth2)):
    user_id = get_user_id(token)
    payload = entry.dict(exclude_unset=True)
    payload["user_id"] = user_id
    resp = supabase.table("emotional_entries").insert(payload).execute()
    data = getattr(resp, 'data', None)
    if not data:
        raise HTTPException(status_code=400, detail="Insert failed")
    return data[0]


@router.get("/entries", response_model=List[EmotionalEntry])
def list_emotional_entries(token: str = Depends(oauth2)):
    user_id = get_user_id(token)
    resp = supabase.table("emotional_entries").select(
        "*").eq("user_id", user_id).order("created_at", desc=True).execute()
    return getattr(resp, 'data', [])


@router.get("/entries/{entry_id}", response_model=EmotionalEntry)
def get_emotional_entry(entry_id: str, token: str = Depends(oauth2)):
    user_id = get_user_id(token)
    resp = supabase.table("emotional_entries").select(
        "*").eq("entry_id", entry_id).eq("user_id", user_id).single().execute()
    data = getattr(resp, 'data', None)
    if not data:
        raise HTTPException(status_code=404, detail="Entry not found")
    return data


@router.patch("/entries/{entry_id}", response_model=EmotionalEntry)
def update_emotional_entry(entry_id: str, entry: EmotionalEntry, token: str = Depends(oauth2)):
    user_id = get_user_id(token)
    resp = supabase.table("emotional_entries").update(entry.dict(
        exclude_unset=True)).eq("entry_id", entry_id).eq("user_id", user_id).execute()
    data = getattr(resp, 'data', None)
    if not data:
        raise HTTPException(status_code=400, detail="Update failed")
    return data[0]


@router.delete("/entries/{entry_id}", response_model=dict)
def delete_emotional_entry(entry_id: str, token: str = Depends(oauth2)):
    user_id = get_user_id(token)
    supabase.table("emotional_entries").delete().eq(
        "entry_id", entry_id).eq("user_id", user_id).execute()
    return {"deleted": True}

# -------------------------------
# CRUD for mood_logs
# -------------------------------


@router.post("/mood-logs", response_model=MoodLog)
def create_mood_log(log: MoodLog, token: str = Depends(oauth2)):
    user_id = get_user_id(token)
    payload = log.dict(exclude_unset=True)
    payload["user_id"] = user_id
    resp = supabase.table("mood_logs").insert(payload).execute()
    data = getattr(resp, 'data', None)
    if not data:
        raise HTTPException(status_code=400, detail="Insert failed")
    return data[0]


@router.get("/mood-logs", response_model=List[MoodLog])
def list_mood_logs(token: str = Depends(oauth2)):
    user_id = get_user_id(token)
    resp = supabase.table("mood_logs").select(
        "*").eq("user_id", user_id).order("created_at", desc=True).execute()
    return getattr(resp, 'data', [])


@router.get("/mood-logs/{log_id}", response_model=MoodLog)
def get_mood_log(log_id: str, token: str = Depends(oauth2)):
    user_id = get_user_id(token)
    resp = supabase.table("mood_logs").select(
        "*").eq("log_id", log_id).eq("user_id", user_id).single().execute()
    data = getattr(resp, 'data', None)
    if not data:
        raise HTTPException(status_code=404, detail="Log not found")
    return data


@router.patch("/mood-logs/{log_id}", response_model=MoodLog)
def update_mood_log(log_id: str, log: MoodLog, token: str = Depends(oauth2)):
    user_id = get_user_id(token)
    resp = supabase.table("mood_logs").update(log.dict(exclude_unset=True)).eq(
        "log_id", log_id).eq("user_id", user_id).execute()
    data = getattr(resp, 'data', None)
    if not data:
        raise HTTPException(status_code=400, detail="Update failed")
    return data[0]


@router.delete("/mood-logs/{log_id}", response_model=dict)
def delete_mood_log(log_id: str, token: str = Depends(oauth2)):
    user_id = get_user_id(token)
    supabase.table("mood_logs").delete().eq(
        "log_id", log_id).eq("user_id", user_id).execute()
    return {"deleted": True}

# -------------------------------
# CRUD for chat_sessions
# -------------------------------


@router.post("/sessions", response_model=ChatSession)
def create_chat_session(session: ChatSession, token: str = Depends(oauth2)):
    user_id = get_user_id(token)
    payload = jsonable_encoder(session, exclude_unset=True, exclude_none=True)
    payload["user_id"] = user_id
    resp = supabase.table("chat_sessions").insert(payload).execute()
    data = getattr(resp, 'data', None)
    if not data:
        raise HTTPException(status_code=400, detail="Insert failed")
    return data[0]


@router.get("/sessions", response_model=List[ChatSession])
def list_chat_sessions(token: str = Depends(oauth2)):
    user_id = get_user_id(token)
    resp = supabase.table("chat_sessions").select(
        "*").eq("user_id", user_id).order("started_at", desc=True).execute()
    return getattr(resp, 'data', [])


@router.get("/sessions/{session_id}", response_model=ChatSession)
def get_chat_session(session_id: str, token: str = Depends(oauth2)):
    user_id = get_user_id(token)
    resp = supabase.table("chat_sessions").select(
        "*").eq("session_id", session_id).eq("user_id", user_id).single().execute()
    data = getattr(resp, 'data', None)
    if not data:
        raise HTTPException(status_code=404, detail="Session not found")
    return data


@router.patch("/sessions/{session_id}", response_model=ChatSession)
def update_chat_session(session_id: str, session: ChatSession, token: str = Depends(oauth2)):
    user_id = get_user_id(token)
    # Allow setting fields to null explicitly (e.g., ended_at=None). Also restrict fields to avoid
    # sending accidental datetimes like started_at.
    raw_payload = jsonable_encoder(
        session, exclude_unset=True, exclude_none=False)
    allowed_keys = {"is_active", "ended_at", "session_title", "session_type"}
    payload = {k: v for k, v in (
        raw_payload or {}).items() if k in allowed_keys}
    resp = supabase.table("chat_sessions").update(payload).eq(
        "session_id", session_id).eq("user_id", user_id).execute()
    data = getattr(resp, 'data', None)
    if not data:
        raise HTTPException(status_code=400, detail="Update failed")
    return data[0]


@router.delete("/sessions/{session_id}", response_model=dict)
def delete_chat_session(session_id: str, token: str = Depends(oauth2)):
    user_id = get_user_id(token)
    supabase.table("chat_sessions").delete().eq(
        "session_id", session_id).eq("user_id", user_id).execute()
    return {"deleted": True}

# -------------------------------
# CRUD for chat_messages
# -------------------------------


@router.post("/messages", response_model=ChatMessage)
def create_chat_message(message: ChatMessage, token: str = Depends(oauth2)):
    user_id = get_user_id(token)
    # Ensure all UUIDs are serialized as strings
    payload = json.loads(message.json(exclude_unset=True))
    # Check session ownership if needed (as in your original logic)
    session = supabase.table("chat_sessions").select("user_id").eq(
        "session_id", payload["session_id"]).single().execute().data
    if not session or session.get("user_id") != user_id:
        raise HTTPException(
            status_code=403, detail="Forbidden: Not your session")
    resp = supabase.table("chat_messages").insert(payload).execute()
    data = getattr(resp, 'data', None)
    if not data:
        raise HTTPException(status_code=400, detail="Insert failed")
    return data[0]


@router.get("/messages/{session_id}", response_model=List[ChatMessage])
def list_chat_messages(session_id: str, token: str = Depends(oauth2)):
    user_id = get_user_id(token)
    # Check session ownership
    session = supabase.table("chat_sessions").select("user_id").eq(
        "session_id", session_id).single().execute().data
    if not session or session.get("user_id") != user_id:
        raise HTTPException(
            status_code=403, detail="Forbidden: Not your session")
    resp = supabase.table("chat_messages").select(
        "*").eq("session_id", session_id).order("timestamp").execute()
    return getattr(resp, 'data', [])


@router.get("/message/{message_id}", response_model=ChatMessage)
def get_chat_message(message_id: str, token: str = Depends(oauth2)):
    # Find the message and check session ownership
    msg = supabase.table("chat_messages").select(
        "*").eq("message_id", message_id).single().execute().data
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found")
    session_id = msg.get("session_id")
    user_id = get_user_id(token)
    session = supabase.table("chat_sessions").select("user_id").eq(
        "session_id", session_id).single().execute().data
    if not session or session.get("user_id") != user_id:
        raise HTTPException(
            status_code=403, detail="Forbidden: Not your session")
    return msg


@router.patch("/message/{message_id}", response_model=ChatMessage)
def update_chat_message(message_id: str, message: ChatMessage, token: str = Depends(oauth2)):
    # Only allow update if session belongs to user
    msg = supabase.table("chat_messages").select(
        "*").eq("message_id", message_id).single().execute().data
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found")
    session_id = msg.get("session_id")
    user_id = get_user_id(token)
    session = supabase.table("chat_sessions").select("user_id").eq(
        "session_id", session_id).single().execute().data
    if not session or session.get("user_id") != user_id:
        raise HTTPException(
            status_code=403, detail="Forbidden: Not your session")
    # Ensure all UUIDs are serialized as strings
    payload = json.loads(message.json(exclude_unset=True))
    resp = supabase.table("chat_messages").update(
        payload).eq("message_id", message_id).execute()
    data = getattr(resp, 'data', None)
    if not data:
        raise HTTPException(status_code=400, detail="Update failed")
    return data[0]


@router.delete("/message/{message_id}", response_model=dict)
def delete_chat_message(message_id: str, token: str = Depends(oauth2)):
    # Only allow delete if session belongs to user
    msg = supabase.table("chat_messages").select(
        "*").eq("message_id", message_id).single().execute().data
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found")
    session_id = msg.get("session_id")
    user_id = get_user_id(token)
    session = supabase.table("chat_sessions").select("user_id").eq(
        "session_id", session_id).single().execute().data
    if not session or session.get("user_id") != user_id:
        raise HTTPException(
            status_code=403, detail="Forbidden: Not your session")
    supabase.table("chat_messages").delete().eq(
        "message_id", message_id).execute()
    return {"deleted": True}

# -------------------------------
# CRUD for emergency_contacts
# -------------------------------


@router.post("/contacts", response_model=EmergencyContact)
def create_emergency_contact(contact: EmergencyContact, token: str = Depends(oauth2)):
    # Optionally, you can restrict this to admin/teacher if needed
    payload = contact.dict(exclude_unset=True)
    resp = supabase.table("emergency_contacts").insert(payload).execute()
    data = getattr(resp, 'data', None)
    if not data:
        raise HTTPException(status_code=400, detail="Insert failed")
    return data[0]


@router.get("/contacts", response_model=List[EmergencyContact])
def list_emergency_contacts(token: str = Depends(oauth2)):
    resp = supabase.table("emergency_contacts").select(
        "*").order("created_at", desc=True).execute()
    return getattr(resp, 'data', [])


@router.get("/contacts/{contact_id}", response_model=EmergencyContact)
def get_emergency_contact(contact_id: str, token: str = Depends(oauth2)):
    resp = supabase.table("emergency_contacts").select(
        "*").eq("contact_id", contact_id).single().execute()
    data = getattr(resp, 'data', None)
    if not data:
        raise HTTPException(status_code=404, detail="Contact not found")
    return data


@router.patch("/contacts/{contact_id}", response_model=EmergencyContact)
def update_emergency_contact(contact_id: str, contact: EmergencyContact, token: str = Depends(oauth2)):
    resp = supabase.table("emergency_contacts").update(contact.dict(
        exclude_unset=True)).eq("contact_id", contact_id).execute()
    data = getattr(resp, 'data', None)
    if not data:
        raise HTTPException(status_code=400, detail="Update failed")
    return data[0]


@router.delete("/contacts/{contact_id}", response_model=dict)
def delete_emergency_contact(contact_id: str, token: str = Depends(oauth2)):
    supabase.table("emergency_contacts").delete().eq(
        "contact_id", contact_id).execute()
    return {"deleted": True}


@router.post("/sessions/{session_id}/auto-reply")
def auto_reply(
    session_id: str,
    user_message: str = Form(""),
    file: UploadFile | None = File(None),
    token: str = Depends(oauth2)
):
    user_id = get_user_id(token)
    # 1. Save user message (reuse create_chat_message logic)
    # If image provided but empty text, store a placeholder
    content_to_store = user_message if user_message else (
        "[Image uploaded]" if file else "")
    user_msg = ChatMessage(
        session_id=session_id,
        sender_type=SenderTypeEnum.user,
        message_content=content_to_store,
    )
    create_chat_message(user_msg, token)
    # 2. Fetch chat history (reuse list_chat_messages logic)
    chat_history = list_chat_messages(session_id, token)
    # 2.1 Load session to detect session_type if present
    session = supabase.table("chat_sessions").select("session_type").eq(
        "session_id", session_id).single().execute().data
    session_type = session.get("session_type") if session else None
    # 3. Call chatbot with chat history
    image_bytes = None
    image_mime = None
    if file is not None:
        image_bytes = file.file.read()
        image_mime = file.content_type
    bot_reply = chat_bot_module.chat_bot(
        chat_history, session_type=session_type, image_bytes=image_bytes, image_mime=image_mime)
    # 4. Save bot reply as a message
    bot_msg = ChatMessage(
        session_id=session_id,
        sender_type=SenderTypeEnum.ai_bot,
        message_content=bot_reply["reply"],
    )
    create_chat_message(bot_msg, token)
    # 5. Return bot reply
    return {"bot_reply": bot_reply}
