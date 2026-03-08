#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
occupation_service.py - Business logic layer for Occupation operations.

Author: Family Tree API Team
Created: 2026-02-23

This module provides business logic for Occupation CRUD operations.

OWASP Secure Coding Practices:
    - Input validation
    - Proper error handling
    - Person ownership validation
"""

from typing import List
from uuid import UUID
from sqlalchemy.orm import Session

from app.repository import occupation_repo, person_repo
from app.schemas.occupation_schema import OccupationCreate, OccupationUpdate


def create_occupation(db: Session, occupation_data: OccupationCreate):
    """
    Create a new occupation for a person.
    
    Args:
        db: Database session
        occupation_data: Occupation creation data
        
    Returns:
        Created Occupation object
        
    Raises:
        ValueError: If person not found
    """
    # Verify person exists
    person = person_repo.get_person_by_id(db, occupation_data.person_id)
    if not person:
        raise ValueError(f"Person with id {occupation_data.person_id} not found")
    
    occupation_dict = occupation_data.model_dump()
    return occupation_repo.create_occupation(db, occupation_dict)


def get_occupation_by_id(db: Session, occupation_id: UUID):
    """
    Get an occupation by ID.
    
    Args:
        db: Database session
        occupation_id: UUID of the occupation
        
    Returns:
        Occupation object
        
    Raises:
        ValueError: If occupation not found
    """
    occupation = occupation_repo.get_occupation_by_id(db, occupation_id)
    if not occupation:
        raise ValueError(f"Occupation with id {occupation_id} not found")
    return occupation


def get_occupations_by_person(db: Session, person_id: UUID) -> List:
    """
    Get all occupations for a person.
    
    Args:
        db: Database session
        person_id: UUID of the person
        
    Returns:
        List of Occupation objects
        
    Raises:
        ValueError: If person not found
    """
    person = person_repo.get_person_by_id(db, person_id)
    if not person:
        raise ValueError(f"Person with id {person_id} not found")
    
    return occupation_repo.get_occupations_by_person(db, person_id)


def update_occupation(db: Session, occupation_id: UUID, occupation_data: OccupationUpdate):
    """
    Update an existing occupation.
    
    Args:
        db: Database session
        occupation_id: UUID of the occupation to update
        occupation_data: Fields to update
        
    Returns:
        Updated Occupation object
        
    Raises:
        ValueError: If occupation not found
    """
    existing = occupation_repo.get_occupation_by_id(db, occupation_id)
    if not existing:
        raise ValueError(f"Occupation with id {occupation_id} not found")
    
    update_dict = occupation_data.model_dump(exclude_unset=True)
    return occupation_repo.update_occupation(db, occupation_id, update_dict)


def delete_occupation(db: Session, occupation_id: UUID) -> bool:
    """
    Delete an occupation.
    
    Args:
        db: Database session
        occupation_id: UUID of the occupation to delete
        
    Returns:
        True if deleted
        
    Raises:
        ValueError: If occupation not found
    """
    existing = occupation_repo.get_occupation_by_id(db, occupation_id)
    if not existing:
        raise ValueError(f"Occupation with id {occupation_id} not found")
    
    return occupation_repo.delete_occupation(db, occupation_id)
