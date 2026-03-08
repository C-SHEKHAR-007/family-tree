#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
address_schema.py - Pydantic schemas for Address model.

Author: Family Tree API Team
Created: 2026-02-23

This module provides request/response schemas for Address endpoints.

OWASP Secure Coding Practices:
    - Input validation via Pydantic
    - Date validation
"""

from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import date, datetime


class AddressCreate(BaseModel):
    """Schema for creating a new address."""
    person_id: UUID = Field(..., description="UUID of the person")
    address_line: str = Field(..., min_length=1, max_length=255)
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    country: Optional[str] = Field(None, max_length=100)
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class AddressUpdate(BaseModel):
    """Schema for updating an address."""
    address_line: Optional[str] = Field(None, min_length=1, max_length=255)
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    country: Optional[str] = Field(None, max_length=100)
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class AddressResponse(BaseModel):
    """Schema for address response."""
    id: UUID
    person_id: UUID
    address_line: str
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    created_at: datetime

    class Config:
        from_attributes = True
