#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
address_repo.py - Repository layer for Address database operations.

Author: Family Tree API Team
Created: 2026-02-23

This module provides database access functions for Address model.

OWASP Secure Coding Practices:
    - Parameterized queries via SQLAlchemy ORM
    - No SQL injection vulnerabilities
    - Proper session management
"""

from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session
from app.models.address import Address


def create_address(db: Session, address_data: dict) -> Address:
    """
    Create a new address in the database.
    
    Args:
        db: Database session
        address_data: Dictionary containing address fields
        
    Returns:
        Created Address object
    """
    address = Address(**address_data)
    db.add(address)
    db.commit()
    db.refresh(address)
    return address


def get_address_by_id(db: Session, address_id: UUID) -> Optional[Address]:
    """
    Retrieve an address by ID.
    
    Args:
        db: Database session
        address_id: UUID of the address
        
    Returns:
        Address object if found, None otherwise
    """
    return db.query(Address).filter(Address.id == address_id).first()


def get_addresses_by_person(db: Session, person_id: UUID) -> List[Address]:
    """
    Get all addresses for a person.
    
    Args:
        db: Database session
        person_id: UUID of the person
        
    Returns:
        List of Address objects
    """
    return db.query(Address).filter(Address.person_id == person_id).all()


def update_address(db: Session, address_id: UUID, address_data: dict) -> Optional[Address]:
    """
    Update an existing address.
    
    Args:
        db: Database session
        address_id: UUID of the address to update
        address_data: Dictionary containing fields to update
        
    Returns:
        Updated Address object if found, None otherwise
    """
    address = get_address_by_id(db, address_id)
    if address:
        for key, value in address_data.items():
            if hasattr(address, key) and value is not None:
                setattr(address, key, value)
        db.commit()
        db.refresh(address)
    return address


def delete_address(db: Session, address_id: UUID) -> bool:
    """
    Delete an address from the database.
    
    Args:
        db: Database session
        address_id: UUID of the address to delete
        
    Returns:
        True if deleted, False if not found
    """
    address = get_address_by_id(db, address_id)
    if address:
        db.delete(address)
        db.commit()
        return True
    return False
