#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
occupation_repo.py - Repository layer for Occupation database operations.

Author: Family Tree API Team
Created: 2026-02-23

This module provides database access functions for Occupation model.

OWASP Secure Coding Practices:
    - Parameterized queries via SQLAlchemy ORM
    - No SQL injection vulnerabilities
    - Proper session management
"""

from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session
from app.models.occupation import Occupation


def create_occupation(db: Session, occupation_data: dict) -> Occupation:
    """
    Create a new occupation in the database.
    
    Args:
        db: Database session
        occupation_data: Dictionary containing occupation fields
        
    Returns:
        Created Occupation object
    """
    occupation = Occupation(**occupation_data)
    db.add(occupation)
    db.commit()
    db.refresh(occupation)
    return occupation


def get_occupation_by_id(db: Session, occupation_id: UUID) -> Optional[Occupation]:
    """
    Retrieve an occupation by ID.
    
    Args:
        db: Database session
        occupation_id: UUID of the occupation
        
    Returns:
        Occupation object if found, None otherwise
    """
    return db.query(Occupation).filter(Occupation.id == occupation_id).first()


def get_occupations_by_person(db: Session, person_id: UUID) -> List[Occupation]:
    """
    Get all occupations for a person.
    
    Args:
        db: Database session
        person_id: UUID of the person
        
    Returns:
        List of Occupation objects
    """
    return db.query(Occupation).filter(Occupation.person_id == person_id).all()


def update_occupation(db: Session, occupation_id: UUID, occupation_data: dict) -> Optional[Occupation]:
    """
    Update an existing occupation.
    
    Args:
        db: Database session
        occupation_id: UUID of the occupation to update
        occupation_data: Dictionary containing fields to update
        
    Returns:
        Updated Occupation object if found, None otherwise
    """
    occupation = get_occupation_by_id(db, occupation_id)
    if occupation:
        for key, value in occupation_data.items():
            if hasattr(occupation, key) and value is not None:
                setattr(occupation, key, value)
        db.commit()
        db.refresh(occupation)
    return occupation


def delete_occupation(db: Session, occupation_id: UUID) -> bool:
    """
    Delete an occupation from the database.
    
    Args:
        db: Database session
        occupation_id: UUID of the occupation to delete
        
    Returns:
        True if deleted, False if not found
    """
    occupation = get_occupation_by_id(db, occupation_id)
    if occupation:
        db.delete(occupation)
        db.commit()
        return True
    return False
