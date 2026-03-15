#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
relationship_routes.py - API routes for Relationship operations.

Author: Family Tree API Team
Created: 2026-02-23

This module provides REST endpoints for managing family relationships.

OWASP Secure Coding Practices:
    - Authentication required for all endpoints
    - Input validation via Pydantic schemas
    - Proper error handling
"""

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user, admin_required, member_or_admin_required
from app.models.user import User
from app.schemas.relationship_schema import (
    RelationshipCreate,
    RelationshipResponse,
    FamilyRelationships,
)
from app.services import relationship_service

router = APIRouter(prefix="/relationships", tags=["Relationships"])


@router.post("/", response_model=RelationshipResponse, status_code=status.HTTP_201_CREATED)
def create_relationship(
    relationship_data: RelationshipCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(member_or_admin_required),
):
    """
    Create a family relationship between two persons in the current user's tree.
    
    Automatically creates inverse relationships where applicable:
    - FATHER/MOTHER creates CHILD relationship
    - SPOUSE creates SPOUSE relationship  
    - SIBLING creates SIBLING relationship
    
    Requires member or admin role. Viewers have read-only access.
    Users can only create relationships within their own tree.
    
    Args:
        relationship_data: Relationship creation data
        db: Database session
        current_user: Authenticated user (member or admin)
        
    Returns:
        Created relationship object
        
    Raises:
        HTTPException: 400 if validation fails or persons not in user's tree
        HTTPException: 403 if user has no tree assigned
    """
    # SUPER_ADMIN can create relationships in any tree
    tree_id = None if current_user.role == "SUPER_ADMIN" else current_user.tree_id
    
    if tree_id is None and current_user.role != "SUPER_ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You must be assigned to a tree to create relationships"
        )
    
    try:
        return relationship_service.create_relationship(db, relationship_data, tree_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=List[RelationshipResponse])
def get_all_relationships(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Max records to return"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get all relationships in the current user's tree with pagination.
    
    SUPER_ADMIN can see all relationships across all trees.
    Other users only see relationships in their own tree.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        db: Database session
        current_user: Authenticated user
        
    Returns:
        List of relationship objects
    """
    # SUPER_ADMIN can see all relationships
    if current_user.role == "SUPER_ADMIN":
        return relationship_service.get_all_relationships(db, skip, limit)
    
    return relationship_service.get_all_relationships(db, skip, limit, current_user.tree_id)


@router.get("/{relationship_id}", response_model=RelationshipResponse)
def get_relationship(
    relationship_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get a relationship by ID within the current user's tree.
    
    SUPER_ADMIN can access any relationship.
    Other users can only access relationships in their own tree.
    
    Args:
        relationship_id: UUID of the relationship
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Relationship object
        
    Raises:
        HTTPException: 404 if relationship not found or not in user's tree
    """
    try:
        tree_id = None if current_user.role == "SUPER_ADMIN" else current_user.tree_id
        return relationship_service.get_relationship_by_id(db, relationship_id, tree_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/person/{person_id}", response_model=List[RelationshipResponse])
def get_person_relationships(
    person_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get all relationships for a specific person in the current user's tree.
    
    SUPER_ADMIN can access relationships for any person.
    Other users can only access relationships for persons in their own tree.
    
    Args:
        person_id: UUID of the person
        db: Database session
        current_user: Authenticated user
        
    Returns:
        List of relationship objects
        
    Raises:
        HTTPException: 404 if person not found or not in user's tree
    """
    try:
        tree_id = None if current_user.role == "SUPER_ADMIN" else current_user.tree_id
        return relationship_service.get_relationships_for_person(db, person_id, tree_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/person/{person_id}/family", response_model=FamilyRelationships)
def get_family_tree(
    person_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get organized family relationships for a person in the current user's tree.
    
    Returns a structured view of:
    - Father, Mother
    - Spouse
    - Children
    - Siblings
    
    SUPER_ADMIN can access any person's family relationships.
    Other users can only access persons in their own tree.
    
    Args:
        person_id: UUID of the person
        db: Database session
        current_user: Authenticated user
        
    Returns:
        FamilyRelationships object with categorized relations
        
    Raises:
        HTTPException: 404 if person not found or not in user's tree
    """
    try:
        tree_id = None if current_user.role == "SUPER_ADMIN" else current_user.tree_id
        return relationship_service.get_family_relationships(db, person_id, tree_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{relationship_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_relationship(
    relationship_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required),
):
    """
    Delete a relationship within the current user's tree.
    
    Requires admin role (SUPER_ADMIN or FAMILY_ADMIN).
    SUPER_ADMIN can delete any relationship.
    FAMILY_ADMIN can only delete relationships in their tree.
    
    Args:
        relationship_id: UUID of the relationship to delete
        db: Database session
        current_user: Authenticated admin user
        
    Raises:
        HTTPException: 404 if relationship not found or not in user's tree
    """
    try:
        tree_id = None if current_user.role == "SUPER_ADMIN" else current_user.tree_id
        relationship_service.delete_relationship(db, relationship_id, tree_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/between/{person_id}/{related_person_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_relationships_between_persons(
    person_id: UUID,
    related_person_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required),
):
    """
    Delete all relationships between two persons in the current user's tree.
    
    Requires admin role (SUPER_ADMIN or FAMILY_ADMIN).
    SUPER_ADMIN can delete relationships between any persons.
    FAMILY_ADMIN can only delete relationships in their tree.
    
    Args:
        person_id: UUID of the first person
        related_person_id: UUID of the second person
        db: Database session
        current_user: Authenticated admin user
        
    Raises:
        HTTPException: 404 if persons not found or not in user's tree
    """
    try:
        tree_id = None if current_user.role == "SUPER_ADMIN" else current_user.tree_id
        relationship_service.delete_relationships_between_persons(
            db, person_id, related_person_id, tree_id
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
