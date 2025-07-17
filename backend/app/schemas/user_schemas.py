from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

class UserDesignation(str, Enum):
    EMPLOYEE = "employee"
    ADMIN = "admin"

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters")
    designation: UserDesignation
    department: str = Field(..., min_length=1, description="Department is required")
    phone_number: Optional[str] = None

    @validator('designation')
    def validate_designation(cls, v):
        if v not in ['employee', 'admin']:
            raise ValueError('Designation must be either "employee" or "admin"')
        return v

class UserResponse(BaseModel):
    id: int
    email: str
    designation: str
    department: str
    phone_number: Optional[str]
    is_master_admin: bool
    is_active: bool
    last_login_time: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int]

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    department: Optional[str] = None
    phone_number: Optional[str] = None
    is_active: Optional[bool] = None

class PasswordChange(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8, description="Password must be at least 8 characters")

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class UserListResponse(BaseModel):
    users: List[UserResponse]
    total: int
    page: int
    per_page: int

class MasterAdminSetup(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    department: str = Field(..., min_length=1)
    phone_number: Optional[str] = None