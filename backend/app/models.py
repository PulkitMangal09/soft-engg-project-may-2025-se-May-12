
from enum import Enum
from pydantic import BaseModel, EmailStr, model_validator, Field
from typing import List, Optional, Literal
from uuid import UUID
from datetime import date, datetime

# ------------------ Auth Models ------------------


class RoleEnum(str, Enum):
    student = "student"
    teacher = "teacher"
    parent = "parent"


class Role(BaseModel):
    id: int
    name: RoleEnum
    description: str


class SignupRequest(BaseModel):
    full_name: str = Field(..., example="Alice Example")
    email:      EmailStr = Field(..., example="alice@example.com")
    password:   str = Field(..., example="Secret123!")
    confirm_password: str = Field(..., example="Secret123!")
    role:       RoleEnum = Field(..., example=RoleEnum.student)
    terms_agreed: bool = Field(..., example=True)

    @model_validator(mode="after")
    def validate(cls, m):
        if m.password != m.confirm_password:
            raise ValueError("Passwords do not match")
        if not m.terms_agreed:
            raise ValueError("You must agree to the terms of service")
        return m


class TokenResponse(BaseModel):
    access_token: str = Field(...,
                              example="eyJhbGciOiJIUzI1NiIsInR5cCI6Ikp...")
    token_type:   str = Field(..., example="bearer")
    role:    str = Field(..., example="student")
    has_profile: Optional[bool] = Field(False, example=False)


# --------------- Emotion Enums ---------------
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
    created_at: Optional[str] = None


class DietEntry(BaseModel):
    id: Optional[UUID] = None
    water_glasses: int
    sodium: float
    sugar: float


class MealEntry(BaseModel):
    id: Optional[UUID] = None
    mealtype: Literal['breakfast', 'lunch', 'dinner', 'snacks']
    description: str
    calories: float
    proteins: float
    carbs: float
    fat: float


class MealCreate(BaseModel):
    mealtype: Literal['breakfast', 'lunch', 'dinner', 'snacks']
    description: str


class HealthMetricsRequest(BaseModel):
    weight: float
    height: float
    systolic: int
    diastolic: int
    blood_sugar: int
    heart_rate: int
    notes: Optional[str] = ""


class HealthMetricsResponse(BaseModel):
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
    time: datetime
    value: float


class TrendResponse(BaseModel):
    weight: List[TrendPoint]
    blood_sugar: List[TrendPoint]
    systolic: List[TrendPoint]
    diastolic: List[TrendPoint]
    heart_rate: List[TrendPoint]
    calories: float
    sugar: float
    sodium: float


class ChildHealthSnapshot(BaseModel):
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


class ChildLinkRequest(BaseModel):
    child_id: UUID
    relationship: str


class ParentDetails(BaseModel):
    parent_id: UUID
    name: str
    is_head: bool
    group: Optional[str]
    description: Optional[str]


class HealthMetric(BaseModel):
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
    child_name: str
    child_id: str
    date: str
    water_glasses: float
    sodium: float
    sugar: float


class Meal_Log(BaseModel):
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
    child_id: UUID
    relationship: str


# Student Finance Models

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


# Teacher Tasks

# --- Pydantic Schemas ---
class TaskBase(BaseModel):
    task_id:       UUID = Field(..., alias="task_id")
    title:         str
    description:   Optional[str] = None
    assigned_to:   UUID
    assigned_by:   UUID
    category:      str
    priority:      Optional[str] = "medium"
    due_date:      Optional[datetime] = None
    due_time:      Optional[str] = None
    status:        Optional[str] = "pending"
    reward_points: Optional[int] = 0
    attachment_url: Optional[str] = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class TaskCreate(BaseModel):
    title:         str
    description:   Optional[str] = None
    category:      str
    priority:      Optional[str] = "medium"
    due_date:      Optional[datetime] = None
    due_time:      Optional[str] = None
    status:        Optional[str] = "pending"
    reward_points: Optional[int] = 0
    attachment_url: Optional[str] = None


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


class Parent(BaseModel):
    group: Optional[str]
    is_head: Optional[bool] = False
    description: Optional[str]
    is_active: Optional[bool] = True
    name: str
# -----------Parent_family-----------------------


class FamilyGroupBase(BaseModel):
    family_name: str = Field(..., example="Smith Family")
    description: Optional[str] = Field(None, example="Our household group")


class FamilyGroupCreate(FamilyGroupBase):
    pass


class FamilyGroup(FamilyGroupBase):
    family_id: UUID
    family_key: str


class FamilyMember(BaseModel):
    member_id: UUID
    user_id:    UUID
    role:       str  # e.g. 'child', 'parent'
    joined_at:  str


class JoinRequestCreate(BaseModel):
    target_id: UUID = Field(..., example="a-family-uuid")
    relationship_type: str = Field(..., example="child")
    message: Optional[str] = Field(None, example="I'd like to join!")

# ----------- Profile Completion Models -----------


class StudentProfileCreate(BaseModel):
    student_number: Optional[str] = Field(None, example="STU123456")
    grade_level: Optional[str] = Field(None, example="10")
    school_name: Optional[str] = Field(None, example="Springfield High School")
    emergency_contact_phone: Optional[str] = Field(None, example="+1234567890")
    can_exist_independently: Optional[bool] = Field(True, example=True)


class TeacherProfileCreate(BaseModel):
    school_name: str = Field(..., example="Springfield High School")
    school_district: str = Field(..., example="Springfield School District")
    subject_grade: Optional[str] = Field(None, example="Mathematics, Grade 10")


class ParentProfileCreate(BaseModel):
    name: str = Field(..., example="John Smith")
    group: Optional[str] = Field(None, example="Smith Family")
    is_head: Optional[bool] = Field(False, example=False)
    description: Optional[str] = Field(None, example="Primary caregiver")


class ProfileCompletionResponse(BaseModel):
    is_completed: bool
    profile_exists: bool
    redirect_url: Optional[str] = None
    message: Optional[str] = None


class ProfileStatusResponse(BaseModel):
    has_profile: bool
    is_completed: bool
    user_type: str
    profile_data: Optional[dict] = None


# -------------- Invitation Codes & Connections ---------------
class InvitationCodeCreate(BaseModel):
    target_type: Literal['family', 'classroom']
    target_id: UUID
    code: Optional[str] = None
    max_uses: Optional[int] = None
    expires_at: Optional[datetime] = None


class InvitationCodeOut(BaseModel):
    code_id: UUID
    code: str
    target_type: str
    target_id: UUID
    created_by: UUID
    expires_at: Optional[str] = None
    max_uses: Optional[int] = None
    created_at: Optional[str] = None


class CodeRedeemRequest(BaseModel):
    code: str
    relationship_type: Optional[str] = None
    message: Optional[str] = None

# -------------- Medical: Conditions, Medications, Logs ---------------
class SeverityEnum(str, Enum):
    mild = "mild"
    moderate = "moderate"
    severe = "severe"


class HealthConditionBase(BaseModel):
    condition_name: str
    severity: SeverityEnum
    diagnosed_date: Optional[date] = None
    doctor_clinic: Optional[str] = None
    dietary_restrictions: Optional[str] = None
    symptoms_to_monitor: Optional[str] = None
    is_active: Optional[bool] = True


class HealthConditionCreate(HealthConditionBase):
    pass


class HealthConditionUpdate(BaseModel):
    condition_name: Optional[str] = None
    severity: Optional[SeverityEnum] = None
    diagnosed_date: Optional[date] = None
    doctor_clinic: Optional[str] = None
    dietary_restrictions: Optional[str] = None
    symptoms_to_monitor: Optional[str] = None
    is_active: Optional[bool] = None


class HealthConditionOut(HealthConditionBase):
    condition_id: UUID
    user_id: Optional[UUID] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class MedicationBase(BaseModel):
    medication_name: str
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    prescribing_doctor: Optional[str] = None
    instructions: Optional[str] = None
    is_active: Optional[bool] = True
    condition_id: Optional[UUID] = None


class MedicationCreate(MedicationBase):
    pass


class MedicationUpdate(BaseModel):
    medication_name: Optional[str] = None
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    prescribing_doctor: Optional[str] = None
    instructions: Optional[str] = None
    is_active: Optional[bool] = None
    condition_id: Optional[UUID] = None


class MedicationOut(MedicationBase):
    medication_id: UUID
    user_id: Optional[UUID] = None
    created_at: Optional[datetime] = None


class MedicationLogCreate(BaseModel):
    taken_at: Optional[datetime] = None
    quantity_taken: Optional[str] = None
    notes: Optional[str] = None


class MedicationLogOut(BaseModel):
    log_id: UUID
    medication_id: UUID
    user_id: Optional[UUID] = None
    taken_at: Optional[datetime] = None
    quantity_taken: Optional[str] = None
    notes: Optional[str] = None
    logged_by: Optional[UUID] = None
