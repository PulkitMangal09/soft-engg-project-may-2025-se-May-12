from enum import Enum
from pydantic import BaseModel, EmailStr, Field, model_validator
from typing import Optional, List
from uuid import UUID
from datetime import datetime, time,date

# ------------------ Auth Models ------------------
class RoleEnum(str, Enum):
    student = "student"
    teacher = "teacher"
    parent  = "parent"

class Role(BaseModel):
    id: int
    name: RoleEnum
    description: str

class SignupRequest(BaseModel):
    full_name: str          = Field(..., example="Alice Example")
    email:      EmailStr    = Field(..., example="alice@example.com")
    password:   str         = Field(..., example="Secret123!")
    confirm_password: str   = Field(..., example="Secret123!")
    role:       RoleEnum    = Field(..., example=RoleEnum.student)
    terms_agreed: bool      = Field(..., example=True)

    @model_validator(mode="after")
    def validate(cls, m):
        if m.password != m.confirm_password:
            raise ValueError("Passwords do not match")
        if not m.terms_agreed:
            raise ValueError("You must agree to the terms of service")
        return m

class TokenResponse(BaseModel):
    access_token: str = Field(..., example="eyJhbGciOiJIUzI1NiIsInR5cCI6Ikp...")
    token_type:   str = Field(..., example="bearer")


# --------------- Emotion Enums ---------------
class MoodEnum(str, Enum):
    very_sad = "very_sad"
    sad = "sad"
    neutral = "neutral"
    happy = "happy"
    very_happy = "very_happy"

class EnergyLevelEnum(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class SleepQualityEnum(str, Enum):
    poor = "poor"
    fair = "fair"
    great = "great"

class StressLevelEnum(str, Enum):
    relaxed = "relaxed"
    moderate = "moderate"
    high = "high"

class PrivacyLevelEnum(str, Enum):
    private = "private"
    anonymous_sharing = "anonymous_sharing"

class SenderTypeEnum(str, Enum):
    user = "user"
    ai_bot = "ai_bot"

class ContactTypeEnum(str, Enum):
    crisis = "crisis"
    teen_support = "teen_support"
    text_line = "text_line"
    bullying = "bullying"
    family_crisis = "family_crisis"
    local_emergency = "local_emergency"


# ---------------- Task Enums ----------------
class TaskCategoryEnum(str, Enum):
    homework = "homework"
    project = "project"
    study = "study"
    personal = "personal"
    chore = "chore"
    health = "health"
    financial = "financial"

class PriorityEnum(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class TaskStatusEnum(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    overdue = "overdue"


# -------------- Data Models ---------------
class EmotionalEntry(BaseModel):
    entry_id: Optional[UUID] = None
    user_id: Optional[UUID] = None
    title: Optional[str] = None
    content: str
    mood: MoodEnum
    intensity: int
    triggers: Optional[List[str]] = []
    tags: Optional[List[str]] = []
    privacy_level: PrivacyLevelEnum = PrivacyLevelEnum.private
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class MoodLog(BaseModel):
    log_id: Optional[UUID] = None
    user_id: Optional[UUID] = None
    mood: MoodEnum
    energy_level: Optional[EnergyLevelEnum] = None
    sleep_quality: Optional[SleepQualityEnum] = None
    stress_level: Optional[StressLevelEnum] = None
    notes: Optional[str] = None
    log_date: Optional[datetime] = None
    created_at: Optional[datetime] = None

class ChatSession(BaseModel):
    session_id: Optional[UUID] = None
    user_id: Optional[UUID] = None
    session_title: Optional[str] = None
    session_type: Optional[str] = None
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    is_active: Optional[bool] = True

class ChatMessage(BaseModel):
    message_id: Optional[UUID] = None
    session_id: UUID
    sender_type: SenderTypeEnum
    message_content: str
    timestamp: Optional[datetime] = None

class EmergencyContact(BaseModel):
    contact_id: Optional[UUID] = None
    name: str
    phone_number: str
    description: Optional[str] = None
    contact_type: ContactTypeEnum
    is_available_24_7: Optional[bool] = True
    created_at: Optional[datetime] = None


# ---------------- Task Models ----------------
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    category: TaskCategoryEnum
    priority: PriorityEnum = PriorityEnum.medium
    due_date: Optional[datetime] = None
    due_time: Optional[time] = None
    status: TaskStatusEnum = TaskStatusEnum.pending
    reward_points: Optional[int] = None
    attachment_url: Optional[str] = None

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    task_id: UUID
    assigned_to: UUID
    assigned_by: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

#Student Finance Models

class TransactionCreate(BaseModel):
    amount: float
    type: str  # "credit" or "debit"
    category: str
    note: Optional[str] = None
    transaction_date: date = Field(default_factory=date.today)

class TransactionOut(BaseModel):
    transaction_id: str
    amount: float
    type: str
    category: str
    note: Optional[str] = None
    transaction_date: date

class SavingsGoalCreate(BaseModel):
    title: str
    target_amount: float
    saved_amount: Optional[float] = 0.0

class SavingsGoalOut(SavingsGoalCreate):
    goal_id: str    


### Teacher Tasks

# --- Pydantic Schemas ---
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    assigned_to: UUID
    assigned_by: UUID
    category: str
    priority: Optional[str] = "medium"
    due_date: Optional[datetime] = None
    due_time: Optional[str] = None
    status: Optional[str] = "pending"
    reward_points: Optional[int] = 0
    attachment_url: Optional[str] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[datetime] = None
    due_time: Optional[str] = None
    status: Optional[str] = None
    reward_points: Optional[int] = None
    attachment_url: Optional[str] = None


class JoinRequestAction(BaseModel):
    student_id: str
    action: str  # "accept" or "reject"