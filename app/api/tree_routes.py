#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tree_routes.py - API routes for Family Tree operations.

Author: Family Tree API Team
Created: 2026-02-23

This module provides REST endpoints for family tree queries and traversal.

OWASP Secure Coding Practices:
    - Authentication required for all endpoints
    - Input validation
    - Depth limits to prevent DoS
"""

from typing import List, Dict, Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.services import tree_service

router = APIRouter(prefix="/tree", tags=["Family Tree"])


@router.get("/{person_id}/ancestors")
def get_ancestors(
    person_id: UUID,
    max_depth: int = Query(5, ge=1, le=10, description="Maximum generations to traverse"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> List[Dict[str, Any]]:
    """
    Get all ancestors of a person.
    
    Returns parents, grandparents, great-grandparents, etc.
    
    Requires authentication.
    
    Args:
        person_id: UUID of the person
        max_depth: Maximum number of generations to traverse (1-10)
        db: Database session
        current_user: Authenticated user
        
    Returns:
        List of ancestor records with generation level
        
    Raises:
        HTTPException: 404 if person not found
    """
    try:
        return tree_service.get_ancestors(db, person_id, max_depth)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/{person_id}/descendants")
def get_descendants(
    person_id: UUID,
    max_depth: int = Query(5, ge=1, le=10, description="Maximum generations to traverse"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> List[Dict[str, Any]]:
    """
    Get all descendants of a person.
    
    Returns children, grandchildren, great-grandchildren, etc.
    
    Requires authentication.
    
    Args:
        person_id: UUID of the person
        max_depth: Maximum number of generations to traverse (1-10)
        db: Database session
        current_user: Authenticated user
        
    Returns:
        List of descendant records with generation level
        
    Raises:
        HTTPException: 404 if person not found
    """
    try:
        return tree_service.get_descendants(db, person_id, max_depth)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/{person_id}/siblings")
def get_siblings(
    person_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> List[Dict[str, Any]]:
    """
    Get all siblings of a person.
    
    Derived from shared parents or direct sibling relationships.
    
    Requires authentication.
    
    Args:
        person_id: UUID of the person
        db: Database session
        current_user: Authenticated user
        
    Returns:
        List of sibling records
        
    Raises:
        HTTPException: 404 if person not found
    """
    try:
        return tree_service.get_siblings(db, person_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/{person_id}/full")
def get_full_tree(
    person_id: UUID,
    depth: int = Query(3, ge=1, le=5, description="Tree depth"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Dict[str, Any]:
    """
    Build a complete family tree starting from a person.
    
    Returns a nested structure with the person, their spouse,
    and children (recursively up to specified depth).
    
    Requires authentication.
    
    Args:
        person_id: UUID of the root person
        depth: How many generations to include (1-5)
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Nested family tree structure
        
    Raises:
        HTTPException: 404 if person not found
    """
    try:
        tree = tree_service.build_family_tree(db, person_id, depth)
        if tree is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Person with id {person_id} not found"
            )
        return tree
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/{person_id}/statistics")
def get_tree_statistics(
    person_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Dict[str, Any]:
    """
    Get statistics about a family tree.
    
    Returns counts of ancestors, descendants, siblings,
    and generation depths.
    
    Requires authentication.
    
    Args:
        person_id: UUID of the root person
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Dictionary with tree statistics
        
    Raises:
        HTTPException: 404 if person not found
    """
    try:
        return tree_service.get_tree_statistics(db, person_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
