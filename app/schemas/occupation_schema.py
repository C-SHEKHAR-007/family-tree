#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
occupation_schema.py - Pydantic schemas for Occupation model.

Author: Family Tree API Team
Created: 2026-02-23

This module provides request/response schemas for Occupation endpoints.

OWASP Secure Coding Practices:
    - Input validation via Pydantic
    - Date validation
"""

from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import date, datetime


class OccupationCreate(BaseModel):
    """Schema for creating a new occupation."""
    person_id: UUID = Field(..., description="UUID of the person")
    title: str = Field(..., min_length=1, max_length=100)
    company: Optional[str] = Field(None, max_length=100)
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class OccupationUpdate(BaseModel):
    """Schema for updating an occupation."""
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    company: Optional[str] = Field(None, max_length=100)
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class OccupationResponse(BaseModel):
    """Schema for occupation response."""
    id: UUID
    person_id: UUID
    title: str
    company: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    created_at: datetime

    class Config:
        from_attributes = True
