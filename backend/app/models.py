from enum import Enum
from pydantic import BaseModel, EmailStr, model_validator

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