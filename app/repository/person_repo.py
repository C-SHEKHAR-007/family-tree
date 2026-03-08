#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
person_repo.py - Repository layer for Person database operations.

Author: Family Tree API Team
Created: 2026-02-23

This module provides database access functions for Person model.

OWASP Secure Coding Practices:
    - Parameterized queries via SQLAlchemy ORM
    - No SQL injection vulnerabilities
    - Proper session management
"""

from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session
from app.models.person import Person


def create_person(db: Session, person_data: dict) -> Person:
    """
    Create a new person in the database.
    
    Args:
        db: Database session
        person_data: Dictionary containing person fields
        
    Returns:
        Created Person object
    """
    person = Person(**person_data)
    db.add(person)
    db.commit()
    db.refresh(person)
    return person


def get_person_by_id(db: Session, person_id: UUID) -> Optional[Person]:
    """
    Retrieve a person by ID.
    
    Args:
        db: Database session
        person_id: UUID of the person
        
    Returns:
        Person object if found, None otherwise
    """
    return db.query(Person).filter(Person.id == person_id).first()


def get_all_persons(db: Session, skip: int = 0, limit: int = 100) -> List[Person]:
    """
    Retrieve all persons with pagination.
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        
    Returns:
        List of Person objects
    """
    return db.query(Person).offset(skip).limit(limit).all()


def update_person(db: Session, person_id: UUID, person_data: dict) -> Optional[Person]:
    """
    Update an existing person.
    
    Args:
        db: Database session
        person_id: UUID of the person to update
        person_data: Dictionary containing fields to update
        
    Returns:
        Updated Person object if found, None otherwise
    """
    person = get_person_by_id(db, person_id)
    if person:
        for key, value in person_data.items():
            if hasattr(person, key) and value is not None:
                setattr(person, key, value)
        db.commit()
        db.refresh(person)
    return person


def delete_person(db: Session, person_id: UUID) -> bool:
    """
    Delete a person from the database.
    
    Args:
        db: Database session
        person_id: UUID of the person to delete
        
    Returns:
        True if deleted, False if person not found
    """
    person = get_person_by_id(db, person_id)
    if person:
        db.delete(person)
        db.commit()
        return True
    return False


def search_persons(
    db: Session,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    gender: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
) -> List[Person]:
    """
    Search persons with filters.
    
    Args:
        db: Database session
        first_name: Optional first name filter
        last_name: Optional last name filter
        gender: Optional gender filter
        skip: Number of records to skip
        limit: Maximum number of records to return
        
    Returns:
        List of matching Person objects
    """
    query = db.query(Person)
    
    if first_name:
        query = query.filter(Person.first_name.ilike(f"%{first_name}%"))
    if last_name:
        query = query.filter(Person.last_name.ilike(f"%{last_name}%"))
    if gender:
        query = query.filter(Person.gender == gender)
    
    return query.offset(skip).limit(limit).all()
