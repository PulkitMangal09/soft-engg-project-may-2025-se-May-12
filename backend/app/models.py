from enum import Enum
from pydantic import BaseModel, EmailStr, model_validator,Field
from typing import List, Optional
from uuid import UUID
from datetime import date,datetime

class RoleEnum(str, Enum):
    student = "student"
    teacher = "teacher"
    parent  = "parent"

class Role(BaseModel):
    id: int
    name: RoleEnum
    description: str

class SignupRequest(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    confirm_password: str
    role: RoleEnum
    terms_agreed: bool

    @model_validator(mode="after")
    def validate(cls, m):
        if m.password != m.confirm_password:
            raise ValueError("Passwords do not match")
        if not m.terms_agreed:
            raise ValueError("You must agree to the terms of service")
        return m

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

# Emotion Management Enums
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

# Emotional Entry Model
class EmotionalEntry(BaseModel):
    entry_id: Optional[UUID] = None
    user_id: Optional[UUID] = None
    title: Optional[str] = None
    content: str
    mood: MoodEnum
    intensity: int
    triggers: Optional[List[str]] = []
    tags: Optional[List[str]] = []
    privacy_level: Optional[PrivacyLevelEnum] = PrivacyLevelEnum.private
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

# Mood Log Model
class MoodLog(BaseModel):
    log_id: Optional[UUID] = None
    user_id: Optional[UUID] = None
    mood: MoodEnum
    energy_level: Optional[EnergyLevelEnum] = None
    sleep_quality: Optional[SleepQualityEnum] = None
    stress_level: Optional[StressLevelEnum] = None
    notes: Optional[str] = None
    log_date: Optional[str] = None
    created_at: Optional[str] = None



# Chat Session Model
class ChatSession(BaseModel):
    session_id: Optional[UUID] = None
    user_id: Optional[UUID] = None
    session_title: Optional[str] = None
    started_at: Optional[str] = None
    ended_at: Optional[str] = None
    is_active: Optional[bool] = True

# Chat Message Model
class ChatMessage(BaseModel):
    message_id: Optional[UUID] = None
    session_id: UUID
    sender_type: SenderTypeEnum
    message_content: str
    timestamp: Optional[str] = None

# Emergency Contact Model
class EmergencyContact(BaseModel):
    contact_id: Optional[UUID] = None
    name: str
    phone_number: str
    description: Optional[str] = None
    contact_type: ContactTypeEnum
    is_available_24_7: Optional[bool] = True
    created_at: Optional[str] = None


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