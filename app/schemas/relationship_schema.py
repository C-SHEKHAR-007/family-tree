#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
relationship_schema.py - Pydantic schemas for Relationship model.

Author: Family Tree API Team
Created: 2026-02-23

This module provides request/response schemas for Relationship endpoints.

OWASP Secure Coding Practices:
    - Input validation via Pydantic
    - Enum validation for relationship types
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from enum import Enum


class RelationshipTypeEnum(str, Enum):
    """Valid relationship types."""
    FATHER = "FATHER"
    MOTHER = "MOTHER"
    SPOUSE = "SPOUSE"
    CHILD = "CHILD"
    SIBLING = "SIBLING"


class RelationshipCreate(BaseModel):
    """Schema for creating a new relationship."""
    person_id: UUID = Field(..., description="UUID of the primary person")
    related_person_id: UUID = Field(..., description="UUID of the related person")
    relationship_type: RelationshipTypeEnum = Field(..., description="Type of relationship")


class RelationshipResponse(BaseModel):
    """Schema for relationship response."""
    id: UUID
    person_id: UUID
    related_person_id: UUID
    relationship_type: str
    created_at: datetime

    class Config:
        from_attributes = True


class RelationshipWithPerson(RelationshipResponse):
    """Relationship with person details."""
    person_name: Optional[str] = None
    related_person_name: Optional[str] = None


class FamilyRelationships(BaseModel):
    """All family relationships for a person."""
    person_id: UUID
    father: Optional[UUID] = None
    mother: Optional[UUID] = None
    spouse: Optional[UUID] = None
    children: List[UUID] = []
    siblings: List[UUID] = []
