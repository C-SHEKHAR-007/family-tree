#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
security.py - Security utilities for authentication and authorization.

Author: Family Tree API Team
Created: 2026-02-23

This module provides:
    - Password hashing using bcrypt
    - JWT token creation and validation
    - OAuth2 authentication scheme
    - RBAC dependencies for route protection

OWASP Secure Coding Practices:
    - Passwords are hashed using bcrypt (never stored plain)
    - JWT tokens have expiration
    - Input validation on token payload
"""

from datetime import datetime, timedelta
from typing import List, Optional

from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from app.core.database import get_db
from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hash a plaintext password using bcrypt.
    
    Args:
        password: Plaintext password to hash
        
    Returns:
        Securely hashed password string
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plaintext password against a hashed password.
    
    Args:
        plain_password: User-provided plaintext password
        hashed_password: Stored hashed password
        
    Returns:
        True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token with payload and expiration.
    
    Args:
        data: Dictionary payload to encode in the token
        expires_delta: Optional custom expiration timedelta
        
    Returns:
        Encoded JWT token string
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """
    Dependency to get the current authenticated user from JWT token.
    
    Args:
        token: JWT token from Authorization header
        db: Database session
        
    Returns:
        User object if token is valid
        
    Raises:
        HTTPException: 401 if token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")

        if user_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    # Fetch user from DB to verify existence and get current role
    from app.models.user import User
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise credentials_exception

    return user


def get_current_active_user(current_user = Depends(get_current_user)):
    """
    Dependency to ensure the current user account is active.
    
    Args:
        current_user: User object from get_current_user
        
    Returns:
        User object if active
        
    Raises:
        HTTPException: 400 if user account is inactive
    """
    # Future: Add is_active check when field is added
    # if not current_user.is_active:
    #     raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def require_role(allowed_roles: List[str]):
    """
    Factory function to create a dependency that checks user roles.
    
    Args:
        allowed_roles: List of role names that are permitted
        
    Returns:
        Dependency function that validates user role
        
    Example:
        @router.delete("/users/{id}")
        def delete_user(..., user=Depends(require_role(["admin"]))):
    """
    def role_checker(current_user = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required role: {', '.join(allowed_roles)}"
            )
        return current_user
    return role_checker


def admin_required(current_user = Depends(get_current_user)):
    """
    Dependency to ensure the current user has admin role.
    
    Args:
        current_user: User object from get_current_user
        
    Returns:
        User object if admin
        
    Raises:
        HTTPException: 403 if user is not admin
    """
    if current_user.role not in ["admin", "SUPER_ADMIN"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user