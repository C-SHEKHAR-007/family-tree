#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
occupation_routes.py - REST API endpoints for Occupation operations.

Author: Family Tree API Team
Created: 2026-02-23

This module provides HTTP endpoints for Occupation CRUD operations.

OWASP Secure Coding Practices:
    - Authentication required for all endpoints
    - Input validation via Pydantic schemas
    - Proper HTTP status codes
    - Error handling
"""

from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.schemas.occupation_schema import OccupationCreate, OccupationUpdate, OccupationResponse
from app.services import occupation_service

router = APIRouter(prefix="/occupations", tags=["Occupations"])


@router.post("/", response_model=OccupationResponse, status_code=status.HTTP_201_CREATED)
def create_occupation(
    occupation_data: OccupationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Create a new occupation for a person.
    
    Requires authentication.
    """
    try:
        occupation = occupation_service.create_occupation(db, occupation_data)
        return occupation
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/{occupation_id}", response_model=OccupationResponse)
def get_occupation(
    occupation_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get an occupation by ID.
    
    Requires authentication.
    """
    try:
        occupation = occupation_service.get_occupation_by_id(db, occupation_id)
        return occupation
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/person/{person_id}", response_model=List[OccupationResponse])
def get_occupations_by_person(
    person_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get all occupations for a person.
    
    Requires authentication.
    """
    try:
        occupations = occupation_service.get_occupations_by_person(db, person_id)
        return occupations
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{occupation_id}", response_model=OccupationResponse)
def update_occupation(
    occupation_id: UUID,
    occupation_data: OccupationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update an existing occupation.
    
    Requires authentication.
    """
    try:
        occupation = occupation_service.update_occupation(db, occupation_id, occupation_data)
        return occupation
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{occupation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_occupation(
    occupation_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Delete an occupation.
    
    Requires authentication.
    """
    try:
        occupation_service.delete_occupation(db, occupation_id)
        return None
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
