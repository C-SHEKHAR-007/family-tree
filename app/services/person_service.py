#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
person_service.py - Business logic layer for Person operations.

Author: Family Tree API Team
Created: 2026-02-23

This module provides business logic for Person CRUD operations.

OWASP Secure Coding Practices:
    - Input validation
    - Proper error handling
    - Data integrity checks
"""

from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session

from app.repository import person_repo
from app.schemas.person_schema import PersonCreate, PersonUpdate


def create_person(db: Session, person_data: PersonCreate, tree_id: UUID = None):
    """
    Create a new person.
    
    Args:
        db: Database session
        person_data: Person creation data
        tree_id: UUID of the tree to assign the person to
        
    Returns:
        Created Person object
    """
    person_dict = person_data.model_dump()
    # Convert enum to string value
    if person_dict.get("gender"):
        person_dict["gender"] = person_dict["gender"].value
    
    # Assign to tree if provided
    if tree_id:
        person_dict["tree_id"] = tree_id
    
    return person_repo.create_person(db, person_dict)


def get_person_by_id(db: Session, person_id: UUID, tree_id: UUID = None):
    """
    Get a person by ID, optionally checking tree ownership.
    
    Args:
        db: Database session
        person_id: UUID of the person
        tree_id: Optional UUID of the tree (for access control)
        
    Returns:
        Person object or None
        
    Raises:
        ValueError: If person not found or doesn't belong to tree
    """
    if tree_id:
        person = person_repo.get_person_by_id_and_tree(db, person_id, tree_id)
        if not person:
            raise ValueError(f"Person with id {person_id} not found in your tree")
    else:
        person = person_repo.get_person_by_id(db, person_id)
        if not person:
            raise ValueError(f"Person with id {person_id} not found")
    return person


def get_all_persons(db: Session, skip: int = 0, limit: int = 100, tree_id: UUID = None):
    """
    Get all persons with pagination, optionally filtered by tree.
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        tree_id: Optional UUID of the tree to filter by
        
    Returns:
        List of Person objects
    """
    if tree_id:
        return person_repo.get_persons_by_tree(db, tree_id, skip, limit)
    return person_repo.get_all_persons(db, skip, limit)


def update_person(db: Session, person_id: UUID, person_data: PersonUpdate, tree_id: UUID = None):
    """
    Update an existing person.
    
    Args:
        db: Database session
        person_id: UUID of the person to update
        person_data: Fields to update
        tree_id: Optional UUID of the tree (for access control)
        
    Returns:
        Updated Person object
        
    Raises:
        ValueError: If person not found or doesn't belong to tree
    """
    # Check if person exists and belongs to tree
    if tree_id:
        existing = person_repo.get_person_by_id_and_tree(db, person_id, tree_id)
        if not existing:
            raise ValueError(f"Person with id {person_id} not found in your tree")
    else:
        existing = person_repo.get_person_by_id(db, person_id)
        if not existing:
            raise ValueError(f"Person with id {person_id} not found")
    
    # Convert to dict, excluding None values
    update_dict = person_data.model_dump(exclude_unset=True)
    
    # Convert enum to string value if present
    if update_dict.get("gender"):
        update_dict["gender"] = update_dict["gender"].value
    
    return person_repo.update_person(db, person_id, update_dict)


def delete_person(db: Session, person_id: UUID, tree_id: UUID = None) -> bool:
    """
    Delete a person.
    
    Args:
        db: Database session
        person_id: UUID of the person to delete
        tree_id: Optional UUID of the tree (for access control)
        
    Returns:
        True if deleted
        
    Raises:
        ValueError: If person not found or doesn't belong to tree
    """
    # Check if person exists and belongs to tree
    if tree_id:
        existing = person_repo.get_person_by_id_and_tree(db, person_id, tree_id)
        if not existing:
            raise ValueError(f"Person with id {person_id} not found in your tree")
    else:
        existing = person_repo.get_person_by_id(db, person_id)
        if not existing:
            raise ValueError(f"Person with id {person_id} not found")
    
    return person_repo.delete_person(db, person_id)


def search_persons(
    db: Session,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    gender: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    tree_id: UUID = None
):
    """
    Search persons with optional filters within a tree.
    
    Args:
        db: Database session
        first_name: Optional first name filter
        last_name: Optional last name filter
        gender: Optional gender filter
        skip: Number of records to skip
        limit: Maximum number of records to return
        tree_id: Optional UUID of the tree to filter by
        
    Returns:
        List of matching Person objects
    """
    return person_repo.search_persons(
        db, first_name, last_name, gender, skip, limit, tree_id
    )
