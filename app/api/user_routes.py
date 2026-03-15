#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
user_routes.py - API routes for User management.

Author: Family Tree API Team
Created: 2026-02-23

User Creation Rules:
    - SUPER_ADMIN can create FAMILY_ADMIN users (new tree owners)
    - FAMILY_ADMIN can create member/viewer users for their own tree
    - SUPER_ADMIN can see all users
    - FAMILY_ADMIN can see only users in their tree
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.schemas.user_schema import UserCreate, UserResponse, UserListItem
from app.core.database import get_db
from app.core.security import get_current_user, hash_password
from app.repository.user_repo import (
    get_user_by_email,
    get_user_by_username,
    create_user,
    get_users_by_tree,
    get_all_users_with_roles,
)
from app.repository.family_tree_repo import create_tree
from app.models.user import User


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_new_user(
    user_data: UserCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new user based on current user's role.
    
    Permission Rules:
    - SUPER_ADMIN can create FAMILY_ADMIN (creates new tree)
    - FAMILY_ADMIN can create member/viewer (for their tree)
    - member/viewer cannot create users
    
    Args:
        user_data: User creation data
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Created user object
        
    Raises:
        HTTPException: 403 if not authorized to create this role
        HTTPException: 400 if validation fails
    """
    # Validate current user's permissions
    if current_user.role not in ["SUPER_ADMIN", "FAMILY_ADMIN", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only SUPER_ADMIN and FAMILY_ADMIN can create users"
        )
    
    # Validate role being created based on current user's role
    requested_role = user_data.role.upper() if user_data.role else ""
    
    if current_user.role == "SUPER_ADMIN":
        # SUPER_ADMIN can only create FAMILY_ADMIN
        if requested_role != "FAMILY_ADMIN":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="SUPER_ADMIN can only create FAMILY_ADMIN users"
            )
    elif current_user.role in ["FAMILY_ADMIN", "admin"]:
        # FAMILY_ADMIN can only create member or viewer for their tree
        if requested_role not in ["MEMBER", "VIEWER"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="FAMILY_ADMIN can only create member or viewer users"
            )
        if not current_user.tree_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You don't have a family tree. Please contact support."
            )
    
    # Check if email already exists
    if get_user_by_email(db, user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Check if username already exists
    if get_user_by_username(db, user_data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Prepare user data
    user_dict = user_data.model_dump()
    user_dict["password_hash"] = hash_password(user_dict.pop("password"))
    user_dict["role"] = requested_role.lower() if requested_role in ["MEMBER", "VIEWER"] else requested_role
    
    # Handle tree assignment based on role
    if requested_role == "FAMILY_ADMIN":
        # Create user first (without tree_id)
        new_user = create_user(db, user_dict)
        
        # Create a new tree for the FAMILY_ADMIN
        tree_data = {
            "name": f"{user_data.last_name} Family Tree",
            "description": f"Family tree for {user_data.first_name} {user_data.last_name}",
            "owner_id": new_user.id,
        }
        new_tree = create_tree(db, tree_data)
        
        # Update user with tree_id
        new_user.tree_id = new_tree.id
        db.commit()
        db.refresh(new_user)
    else:
        # member/viewer - assign to current user's tree
        user_dict["tree_id"] = current_user.tree_id
        new_user = create_user(db, user_dict)
    
    return new_user


@router.get("/", response_model=List[UserListItem])
def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List users based on current user's role.
    
    - SUPER_ADMIN sees all users
    - FAMILY_ADMIN sees only users in their tree
    - member/viewer cannot list users
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        db: Database session
        current_user: Authenticated user
        
    Returns:
        List of users
    """
    if current_user.role == "SUPER_ADMIN":
        # SUPER_ADMIN can see all users
        return get_all_users_with_roles(db, skip, limit)
    elif current_user.role in ["FAMILY_ADMIN", "admin"]:
        # FAMILY_ADMIN can see users in their tree
        if not current_user.tree_id:
            return []
        return get_users_by_tree(db, current_user.tree_id, skip, limit)
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to list users"
        )


@router.get("/me/tree-users", response_model=List[UserListItem])
def get_my_tree_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all users in the current user's tree.
    
    Only FAMILY_ADMIN can access this endpoint.
    
    Args:
        db: Database session
        current_user: Authenticated user
        
    Returns:
        List of users in the tree
    """
    if current_user.role not in ["FAMILY_ADMIN", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only FAMILY_ADMIN can view tree users"
        )
    
    if not current_user.tree_id:
        return []
    
    return get_users_by_tree(db, current_user.tree_id)

