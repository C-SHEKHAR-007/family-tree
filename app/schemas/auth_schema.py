#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
auth_schema.py - Pydantic schemas for authentication.

Author: Family Tree API Team
Created: 2026-02-23

This module provides request/response schemas for authentication endpoints.

OWASP Secure Coding Practices:
    - Input validation via Pydantic
    - Email validation using EmailStr
    - Password minimum length requirement
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from uuid import UUID
from datetime import datetime


class Token(BaseModel):
    """JWT token response schema."""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Token payload data schema."""
    sub: str | None = None
    email: str | None = None
    role: str | None = None


class UserRegister(BaseModel):
    """User registration request schema."""
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    mobile: Optional[str] = Field(None, max_length=20)
    password: str = Field(..., min_length=8, description="Minimum 8 characters")


class UserProfile(BaseModel):
    """User profile response schema."""
    id: UUID
    first_name: str
    last_name: str
    email: EmailStr
    username: str
    mobile: Optional[str]
    role: str
    person_id: Optional[UUID] = None
    family_root_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    """Alternative login request schema (not using OAuth2 form)."""
    email: EmailStr
    password: str