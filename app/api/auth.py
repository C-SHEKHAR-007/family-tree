#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
auth.py - Authentication routes for login, registration, and profile.

Author: Family Tree API Team
Created: 2026-02-23

This module provides:
    - POST /auth/login - User login with JWT token generation
    - POST /auth/register - User registration
    - GET /auth/me - Get current user profile

OWASP Secure Coding Practices:
    - Password verification using bcrypt
    - JWT tokens with expiration
    - Input validation via Pydantic schemas
    - Proper error handling without leaking sensitive info
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import (
    verify_password,
    create_access_token,
    hash_password,
    get_current_user,
)
from app.repository.user_repo import get_user_by_email, create_user, get_user_by_username
from app.schemas.auth_schema import Token, UserRegister, UserProfile
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    Authenticate user and return JWT access token.
    
    Uses OAuth2 password flow - username field contains email.
    
    Args:
        form_data: OAuth2 form with username (email) and password
        db: Database session
        
    Returns:
        Token with access_token and token_type
        
    Raises:
        HTTPException: 401 if credentials are invalid
    """
    user = get_user_by_email(db, form_data.username)

    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "email": user.email,
            "role": user.role
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.post("/register", response_model=UserProfile, status_code=status.HTTP_201_CREATED)
def register(
    user_data: UserRegister,
    db: Session = Depends(get_db),
):
    """
    Register a new user account.
    
    Args:
        user_data: User registration data
        db: Database session
        
    Returns:
        Created user profile
        
    Raises:
        HTTPException: 400 if email or username already exists
    """
    # Check if email already exists
    existing_email = get_user_by_email(db, user_data.email)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Check if username already exists
    existing_username = get_user_by_username(db, user_data.username)
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Create user with hashed password
    user_dict = user_data.model_dump()
    user_dict["password_hash"] = hash_password(user_dict.pop("password"))
    user_dict["role"] = "member"  # Default role for new users
    
    new_user = create_user(db, user_dict)
    
    return new_user


@router.get("/me", response_model=UserProfile)
def get_me(current_user: User = Depends(get_current_user)):
    """
    Get current authenticated user's profile.
    
    Args:
        current_user: User object from JWT token
        
    Returns:
        Current user profile information
    """
    return current_user