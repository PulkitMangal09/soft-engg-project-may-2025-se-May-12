from enum import Enum
from typing import List, Optional, Literal
from uuid import UUID
from datetime import date, datetime

from pydantic import BaseModel, EmailStr, Field, model_validator
from pydantic.config import ConfigDict

# =========================================================
#                       Auth Models
# =========================================================

class RoleEnum(str, Enum):
    student = "student"
    teacher = "teacher"
    parent  = "parent"


class Role(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: RoleEnum
    description: str


class SignupRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    full_name: str = Field(..., example="Alice Example")
    email: EmailStr = Field(..., example="alice@example.com")
    password: str = Field(..., example="Secret123!")
    confirm_password: str = Field(..., example="Secret123!")
    role: RoleEnum = Field(..., example=RoleEnum.student)
    terms_agreed: bool = Field(..., example=True)

    @model_validator(mode="after")
    def validate(cls, m):
        if m.password != m.confirm_password:
            raise ValueError("Passwords do not match")
        if not m.terms_agreed:
            raise ValueError("You must agree to the terms of service")
        return m


class TokenResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    access_token: str = Field(..., example="eyJhbGciOiJIUzI1NiIsInR5cCI6Ikp...")
    token_type: str = Field(..., example="bearer")
    role: str = Field(..., example="student")
    has_profile: Optional[bool] = Field(False, example=False)


# =========================================================
#                   Emotion / Wellbeing
# =========================================================

class MoodEnum(str, Enum):
    neutral = "neutral"
    anxious = "anxious"
    excited = "excited"
    sad = "sad"
    happy = "happy"
    angry = "angry"


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


class EmotionalEntry(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    entry_id: Optional[UUID] = None
    user_id: Optional[UUID] = None
    title: Optional[str] = None
    content: str
    mood: MoodEnum
    intensity: int
    triggers: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    privacy_level: PrivacyLevelEnum = PrivacyLevelEnum.private
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class MoodLog(BaseModel):
    model_config = ConfigDict(from_attributes=True)

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
    model_config = ConfigDict(from_attributes=True)

    session_id: Optional[UUID] = None
    user_id: Optional[UUID] = None
    session_title: Optional[str] = None
    session_type: Optional[str] = None
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    is_active: Optional[bool] = True


class ChatMessage(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    message_id: Optional[UUID] = None
    session_id: UUID
    sender_type: SenderTypeEnum
    message_content: str
    timestamp: Optional[datetime] = None


class EmergencyContact(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    contact_id: Optional[UUID] = None
    name: str
    phone_number: str
    description: Optional[str] = None
    contact_type: ContactTypeEnum
    is_available_24_7: Optional[bool] = True
    created_at: Optional[str] = None


# =========================================================
#                        Nutrition
# =========================================================

class DietEntry(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[UUID] = None
    water_glasses: int
    sodium: float
    sugar: float


class MealEntry(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[UUID] = None
    mealtype: Literal['breakfast', 'lunch', 'dinner', 'snacks']
    description: str
    calories: float
    proteins: float
    carbs: float
    fat: float


class MealCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    mealtype: Literal['breakfast', 'lunch', 'dinner', 'snacks']
    description: str


# =========================================================
#                         Health
# =========================================================

class HealthMetricsRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    weight: float
    height: float
    systolic: int
    diastolic: int
    blood_sugar: int
    heart_rate: int
    notes: Optional[str] = ""


class HealthMetricsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    weight: float
    height: float
    bmi: float
    systolic: int
    diastolic: int
    blood_sugar: int
    heart_rate: int
    notes: Optional[str]
    time: datetime


class TrendPoint(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    time: datetime
    value: float


class TrendResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    weight: List[TrendPoint]
    blood_sugar: List[TrendPoint]
    systolic: List[TrendPoint]
    diastolic: List[TrendPoint]
    heart_rate: List[TrendPoint]
    calories: float
    sugar: float
    sodium: float


class ChildHealthSnapshot(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    full_name: str
    weight: float
    height: float
    bmi: float
    systolic: int
    diastolic: int
    blood_sugar: int
    heart_rate: int
    notes: str
    created_at: str


# =========================================================
#                     Family / Parents
# =========================================================

class ChildLinkRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    child_id: UUID
    relationship: str


class ParentDetails(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    parent_id: UUID
    name: str
    is_head: bool
    group: Optional[str]
    description: Optional[str]


# 👇 **Re-added to satisfy `from ..models import Parent`**
class Parent(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    group: Optional[str] = None
    is_head: Optional[bool] = False
    description: Optional[str] = None
    is_active: Optional[bool] = True


class HealthMetric(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    student_id: str
    weight: float
    height: float
    systolic: float
    diastolic: float
    bmi: float
    created_at: datetime
    blood_sugar: float
    notes: str
    heart_rate: int


class ChildDietLog(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    child_name: str
    child_id: str
    date: str
    water_glasses: float
    sodium: float
    sugar: float


class Meal_Log(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    student_id: str
    time: datetime
    mealtype: str
    description: str
    calories: float
    proteins: float
    carbs: float
    fat: float


class UpdateChildLink(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    child_id: UUID
    relationship: str


# =========================================================
#                      Student Finance
# =========================================================

class TransactionCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    amount: float
    type: str  # "credit" or "debit"
    category: str
    note: Optional[str] = None
    transaction_date: date = Field(default_factory=date.today)


class TransactionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    transaction_id: str
    amount: float
    type: str
    category: str
    note: Optional[str] = None
    transaction_date: date


class SavingsGoalCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    target_amount: float
    saved_amount: Optional[float] = 0.0


class SavingsGoalOut(SavingsGoalCreate):
    model_config = ConfigDict(from_attributes=True)

    goal_id: str


# =========================================================
#                          Tasks
# =========================================================

class TaskCategoryEnum(str, Enum):
    homework   = "homework"
    project    = "project"
    study      = "study"
    personal   = "personal"
    chore      = "chore"
    health     = "health"
    financial  = "financial"


class PriorityEnum(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class TaskStatusEnum(str, Enum):
    pending     = "pending"
    in_progress = "in_progress"
    completed   = "completed"
    overdue     = "overdue"


class TaskBase(BaseModel):
    """Common user-editable fields."""
    model_config = ConfigDict(from_attributes=True, validate_by_name=True)

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
    """Create payload (server will add task_id/created_at)."""
    model_config = ConfigDict(from_attributes=True)


class TaskUpdate(BaseModel):
    """Patch/put payload (all optional)."""
    model_config = ConfigDict(from_attributes=True)

    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[datetime] = None
    due_time: Optional[str] = None
    status: Optional[str] = None
    reward_points: Optional[int] = None
    attachment_url: Optional[str] = None


class TaskOut(TaskBase):
    """Row returned from DB."""
    model_config = ConfigDict(from_attributes=True, validate_by_name=True)

    task_id: UUID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class JoinRequestAction(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    student_id: str
    action: str  # "accept" or "reject"


# =========================================================
#                       Family Groups
# =========================================================

class FamilyGroupBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    family_name: str = Field(..., example="Smith Family")
    description: Optional[str] = Field(None, example="Our household group")


class FamilyGroupCreate(FamilyGroupBase):
    pass


class FamilyGroup(FamilyGroupBase):
    model_config = ConfigDict(from_attributes=True)

    family_id: UUID
    family_key: str


class FamilyMember(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    member_id: UUID
    user_id: UUID
    role: str  # e.g. 'child', 'parent'
    joined_at: str


class JoinRequestCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    target_id: UUID = Field(..., example="a-family-uuid")
    relationship_type: str = Field(..., example="child")
    message: Optional[str] = Field(None, example="I'd like to join!")


# =========================================================
#                    Profile Completion
# =========================================================

class StudentProfileCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    student_number: Optional[str] = Field(None, example="STU123456")
    grade_level: Optional[str] = Field(None, example="10")
    school_name: Optional[str] = Field(None, example="Springfield High School")
    emergency_contact_phone: Optional[str] = Field(None, example="+1234567890")
    can_exist_independently: Optional[bool] = Field(True, example=True)


class TeacherProfileCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    school_name: str = Field(..., example="Springfield High School")
    school_district: str = Field(..., example="Springfield School District")
    subject_grade: Optional[str] = Field(None, example="Mathematics, Grade 10")


class ParentProfileCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(..., example="John Smith")
    group: Optional[str] = Field(None, example="Smith Family")
    is_head: Optional[bool] = Field(False, example=False)
    description: Optional[str] = Field(None, example="Primary caregiver")


class ProfileCompletionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    is_completed: bool
    profile_exists: bool
    redirect_url: Optional[str] = None
    message: Optional[str] = None


class ProfileStatusResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    has_profile: bool
    is_completed: bool
    user_type: str
    profile_data: Optional[dict] = None


# =========================================================
#            Invitation Codes & Connections
# =========================================================

class InvitationCodeCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    target_type: Literal['family', 'classroom']
    target_id: UUID
    code: Optional[str] = None
    max_uses: Optional[int] = None
    expires_at: Optional[datetime] = None


class InvitationCodeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    code_id: UUID
    code: str
    target_type: str
    target_id: UUID
    created_by: UUID
    expires_at: Optional[str] = None
    max_uses: Optional[int] = None
    created_at: Optional[str] = None


class CodeRedeemRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    code: str
    relationship_type: Optional[str] = None
    message: Optional[str] = None
