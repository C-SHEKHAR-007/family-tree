#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
user_repo.py - Repository layer for User database operations.

Author: Family Tree API Team
Created: 2026-02-23

This module provides database access functions for User model.

OWASP Secure Coding Practices:
    - Parameterized queries via SQLAlchemy ORM
    - No SQL injection vulnerabilities
    - Proper session management
"""

from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session
from app.models.user import User


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """
    Retrieve a user by email address.
    
    Args:
        db: Database session
        email: Email address to search
        
    Returns:
        User object if found, None otherwise
    """
    return db.query(User).filter(User.email == email).first()


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """
    Retrieve a user by username.
    
    Args:
        db: Database session
        username: Username to search
        
    Returns:
        User object if found, None otherwise
    """
    return db.query(User).filter(User.username == username).first()


def get_user_by_id(db: Session, user_id: UUID) -> Optional[User]:
    """
    Retrieve a user by ID.
    
    Args:
        db: Database session
        user_id: UUID of the user
        
    Returns:
        User object if found, None otherwise
    """
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, user_data: dict) -> User:
    """
    Create a new user in the database.
    
    Args:
        db: Database session
        user_data: Dictionary containing user fields
        
    Returns:
        Created User object
    """
    user = User(**user_data)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_all_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    """
    Retrieve all users with pagination.
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        
    Returns:
        List of User objects
    """
    return db.query(User).offset(skip).limit(limit).all()


def update_user(db: Session, user_id: UUID, user_data: dict) -> Optional[User]:
    """
    Update an existing user.
    
    Args:
        db: Database session
        user_id: UUID of the user to update
        user_data: Dictionary containing fields to update
        
    Returns:
        Updated User object if found, None otherwise
    """
    user = get_user_by_id(db, user_id)
    if user:
        for key, value in user_data.items():
            if hasattr(user, key):
                setattr(user, key, value)
        db.commit()
        db.refresh(user)
    return user


def delete_user(db: Session, user_id: UUID) -> bool:
    """
    Delete a user from the database.
    
    Args:
        db: Database session
        user_id: UUID of the user to delete
        
    Returns:
        True if deleted, False if user not found
    """
    user = get_user_by_id(db, user_id)
    if user:
        db.delete(user)
        db.commit()
        return True
    return False