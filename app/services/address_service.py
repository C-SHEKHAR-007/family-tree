#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
address_service.py - Business logic layer for Address operations.

Author: Family Tree API Team
Created: 2026-02-23

This module provides business logic for Address CRUD operations.

OWASP Secure Coding Practices:
    - Input validation
    - Proper error handling
    - Person ownership validation
"""

from typing import List
from uuid import UUID
from sqlalchemy.orm import Session

from app.repository import address_repo, person_repo
from app.schemas.address_schema import AddressCreate, AddressUpdate


def create_address(db: Session, address_data: AddressCreate):
    """
    Create a new address for a person.
    
    Args:
        db: Database session
        address_data: Address creation data
        
    Returns:
        Created Address object
        
    Raises:
        ValueError: If person not found
    """
    # Verify person exists
    person = person_repo.get_person_by_id(db, address_data.person_id)
    if not person:
        raise ValueError(f"Person with id {address_data.person_id} not found")
    
    address_dict = address_data.model_dump()
    return address_repo.create_address(db, address_dict)


def get_address_by_id(db: Session, address_id: UUID):
    """
    Get an address by ID.
    
    Args:
        db: Database session
        address_id: UUID of the address
        
    Returns:
        Address object
        
    Raises:
        ValueError: If address not found
    """
    address = address_repo.get_address_by_id(db, address_id)
    if not address:
        raise ValueError(f"Address with id {address_id} not found")
    return address


def get_addresses_by_person(db: Session, person_id: UUID) -> List:
    """
    Get all addresses for a person.
    
    Args:
        db: Database session
        person_id: UUID of the person
        
    Returns:
        List of Address objects
        
    Raises:
        ValueError: If person not found
    """
    person = person_repo.get_person_by_id(db, person_id)
    if not person:
        raise ValueError(f"Person with id {person_id} not found")
    
    return address_repo.get_addresses_by_person(db, person_id)


def update_address(db: Session, address_id: UUID, address_data: AddressUpdate):
    """
    Update an existing address.
    
    Args:
        db: Database session
        address_id: UUID of the address to update
        address_data: Fields to update
        
    Returns:
        Updated Address object
        
    Raises:
        ValueError: If address not found
    """
    existing = address_repo.get_address_by_id(db, address_id)
    if not existing:
        raise ValueError(f"Address with id {address_id} not found")
    
    update_dict = address_data.model_dump(exclude_unset=True)
    return address_repo.update_address(db, address_id, update_dict)


def delete_address(db: Session, address_id: UUID) -> bool:
    """
    Delete an address.
    
    Args:
        db: Database session
        address_id: UUID of the address to delete
        
    Returns:
        True if deleted
        
    Raises:
        ValueError: If address not found
    """
    existing = address_repo.get_address_by_id(db, address_id)
    if not existing:
        raise ValueError(f"Address with id {address_id} not found")
    
    return address_repo.delete_address(db, address_id)
