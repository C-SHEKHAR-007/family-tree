#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
address_routes.py - REST API endpoints for Address operations.

Author: Family Tree API Team
Created: 2026-02-23

This module provides HTTP endpoints for Address CRUD operations.

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
from app.schemas.address_schema import AddressCreate, AddressUpdate, AddressResponse
from app.services import address_service

router = APIRouter(prefix="/addresses", tags=["Addresses"])


@router.post("/", response_model=AddressResponse, status_code=status.HTTP_201_CREATED)
def create_address(
    address_data: AddressCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Create a new address for a person.
    
    Requires authentication.
    """
    try:
        address = address_service.create_address(db, address_data)
        return address
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/{address_id}", response_model=AddressResponse)
def get_address(
    address_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get an address by ID.
    
    Requires authentication.
    """
    try:
        address = address_service.get_address_by_id(db, address_id)
        return address
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/person/{person_id}", response_model=List[AddressResponse])
def get_addresses_by_person(
    person_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get all addresses for a person.
    
    Requires authentication.
    """
    try:
        addresses = address_service.get_addresses_by_person(db, person_id)
        return addresses
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{address_id}", response_model=AddressResponse)
def update_address(
    address_id: UUID,
    address_data: AddressUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update an existing address.
    
    Requires authentication.
    """
    try:
        address = address_service.update_address(db, address_id, address_data)
        return address
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_address(
    address_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Delete an address.
    
    Requires authentication.
    """
    try:
        address_service.delete_address(db, address_id)
        return None
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
