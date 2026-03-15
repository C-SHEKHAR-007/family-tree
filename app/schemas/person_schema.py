#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
person_schema.py - Pydantic schemas for Person model.

Author: Family Tree API Team
Created: 2026-02-23

This module provides request/response schemas for Person endpoints.

OWASP Secure Coding Practices:
    - Input validation via Pydantic
    - Email validation using EmailStr
    - Date validation
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from uuid import UUID
from datetime import date, datetime
from enum import Enum


class GenderEnum(str, Enum):
    """Gender enumeration."""
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"


class PersonCreate(BaseModel):
    """Schema for creating a new person."""
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    gender: GenderEnum
    date_of_birth: Optional[date] = None
    mobile: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    birth_place: Optional[str] = Field(None, max_length=255)


class PersonUpdate(BaseModel):
    """Schema for updating a person."""
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    gender: Optional[GenderEnum] = None
    date_of_birth: Optional[date] = None
    mobile: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    birth_place: Optional[str] = Field(None, max_length=255)


class PersonResponse(BaseModel):
    """Schema for person response."""
    id: UUID
    first_name: str
    last_name: str
    gender: str
    date_of_birth: Optional[date] = None
    mobile: Optional[str] = None
    email: Optional[str] = None
    birth_place: Optional[str] = None
    tree_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PersonBrief(BaseModel):
    """Brief person info for relationship responses."""
    id: UUID
    first_name: str
    last_name: str
    gender: str

    class Config:
        from_attributes = True


class PersonWithRelations(PersonResponse):
    """Person with family relationships."""
    father: Optional[PersonBrief] = None
    mother: Optional[PersonBrief] = None
    spouse: Optional[PersonBrief] = None
    children: List[PersonBrief] = []
    siblings: List[PersonBrief] = []
