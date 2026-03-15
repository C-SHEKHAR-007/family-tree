from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from datetime import datetime
from typing import Optional, List


class UserCreate(BaseModel):
    """Schema for creating a user."""
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    mobile: Optional[str] = Field(None, max_length=20)
    password: str = Field(..., min_length=8)
    role: str = Field(..., description="Role: FAMILY_ADMIN, member, or viewer")


class UserResponse(BaseModel):
    """User response schema with tree information."""
    id: UUID
    first_name: str
    last_name: str
    email: EmailStr
    username: str
    mobile: Optional[str]
    role: str
    tree_id: Optional[UUID] = None
    created_at: datetime

    class Config:
        from_attributes = True


class UserListItem(BaseModel):
    """Simplified user item for list views (SUPER_ADMIN)."""
    id: UUID
    first_name: str
    last_name: str
    email: EmailStr
    username: str
    role: str
    tree_id: Optional[UUID] = None
    created_at: datetime

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"