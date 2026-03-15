#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
person_routes.py - API routes for Person CRUD operations.

Author: Family Tree API Team
Created: 2026-02-23

This module provides REST endpoints for managing persons.

OWASP Secure Coding Practices:
    - Authentication required for all endpoints
    - Input validation via Pydantic schemas
    - Proper error handling
"""

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user, admin_required, member_or_admin_required
from app.models.user import User
from app.schemas.person_schema import (
    PersonCreate,
    PersonUpdate,
    PersonResponse,
)
from app.services import person_service

router = APIRouter(prefix="/persons", tags=["Persons"])


@router.post("/", response_model=PersonResponse, status_code=status.HTTP_201_CREATED)
def create_person(
    person_data: PersonCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(member_or_admin_required),
):
    """
    Create a new person in the current user's tree.
    
    Requires member or admin role. Viewers have read-only access.
    Person is automatically assigned to the current user's tree.
    
    Args:
        person_data: Person creation data
        db: Database session
        current_user: Authenticated user (member or admin)
        
    Returns:
        Created person object
    """
    if not current_user.tree_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You don't have a family tree. Please contact support."
        )
    return person_service.create_person(db, person_data, current_user.tree_id)


@router.get("/", response_model=List[PersonResponse])
def get_all_persons(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Max records to return"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get all persons in the current user's tree with pagination.
    
    SUPER_ADMIN can see all persons across all trees.
    Other users only see persons in their own tree.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        db: Database session
        current_user: Authenticated user
        
    Returns:
        List of person objects
    """
    # SUPER_ADMIN can see all persons
    if current_user.role == "SUPER_ADMIN":
        return person_service.get_all_persons(db, skip, limit)
    
    # Others see only their tree's persons
    return person_service.get_all_persons(db, skip, limit, current_user.tree_id)


@router.get("/search", response_model=List[PersonResponse])
def search_persons(
    first_name: Optional[str] = Query(None, description="Filter by first name"),
    last_name: Optional[str] = Query(None, description="Filter by last name"),
    gender: Optional[str] = Query(None, description="Filter by gender"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Search persons with filters within the current user's tree.
    
    SUPER_ADMIN can search across all trees.
    Other users only search within their own tree.
    
    Args:
        first_name: Optional first name filter
        last_name: Optional last name filter
        gender: Optional gender filter
        skip: Number of records to skip
        limit: Maximum number of records to return
        db: Database session
        current_user: Authenticated user
        
    Returns:
        List of matching person objects
    """
    # SUPER_ADMIN can search all trees
    tree_id = None if current_user.role == "SUPER_ADMIN" else current_user.tree_id
    return person_service.search_persons(
        db, first_name, last_name, gender, skip, limit, tree_id
    )


@router.get("/{person_id}", response_model=PersonResponse)
def get_person(
    person_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get a person by ID within the current user's tree.
    
    SUPER_ADMIN can access any person.
    Other users can only access persons in their own tree.
    
    Args:
        person_id: UUID of the person
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Person object
        
    Raises:
        HTTPException: 404 if person not found or not in user's tree
    """
    try:
        # SUPER_ADMIN can access any person
        tree_id = None if current_user.role == "SUPER_ADMIN" else current_user.tree_id
        return person_service.get_person_by_id(db, person_id, tree_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{person_id}", response_model=PersonResponse)
def update_person(
    person_id: UUID,
    person_data: PersonUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(member_or_admin_required),
):
    """
    Update a person within the current user's tree.
    
    Requires member or admin role. Viewers have read-only access.
    Users can only update persons in their own tree.
    
    Args:
        person_id: UUID of the person to update
        person_data: Fields to update
        db: Database session
        current_user: Authenticated user (member or admin)
        
    Returns:
        Updated person object
        
    Raises:
        HTTPException: 404 if person not found or not in user's tree
    """
    try:
        # Verify person belongs to user's tree (SUPER_ADMIN can update any)
        tree_id = None if current_user.role == "SUPER_ADMIN" else current_user.tree_id
        return person_service.update_person(db, person_id, person_data, tree_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{person_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_person(
    person_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required),
):
    """
    Delete a person within the current user's tree.
    
    Requires admin role (SUPER_ADMIN or FAMILY_ADMIN).
    Admins can only delete persons in their own tree.
    SUPER_ADMIN can delete persons from any tree.
    
    Args:
        person_id: UUID of the person to delete
        db: Database session
        current_user: Authenticated admin user
        
    Raises:
        HTTPException: 404 if person not found or not in user's tree
    """
    try:
        # SUPER_ADMIN can delete any person
        tree_id = None if current_user.role == "SUPER_ADMIN" else current_user.tree_id
        person_service.delete_person(db, person_id, tree_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
