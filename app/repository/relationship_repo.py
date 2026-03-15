#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
relationship_repo.py - Repository layer for Relationship database operations.

Author: Family Tree API Team
Created: 2026-02-23

This module provides database access functions for Relationship model.

OWASP Secure Coding Practices:
    - Parameterized queries via SQLAlchemy ORM
    - No SQL injection vulnerabilities
    - Proper session management
"""

from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.relationship import Relationship


def create_relationship(db: Session, relationship_data: dict) -> Relationship:
    """
    Create a new relationship in the database.
    
    Args:
        db: Database session
        relationship_data: Dictionary containing relationship fields
        
    Returns:
        Created Relationship object
    """
    relationship = Relationship(**relationship_data)
    db.add(relationship)
    db.commit()
    db.refresh(relationship)
    return relationship


def get_relationship_by_id(db: Session, relationship_id: UUID) -> Optional[Relationship]:
    """
    Retrieve a relationship by ID.
    
    Args:
        db: Database session
        relationship_id: UUID of the relationship
        
    Returns:
        Relationship object if found, None otherwise
    """
    return db.query(Relationship).filter(Relationship.id == relationship_id).first()


def get_relationships_by_person(db: Session, person_id: UUID) -> List[Relationship]:
    """
    Get all relationships for a person.
    
    Args:
        db: Database session
        person_id: UUID of the person
        
    Returns:
        List of Relationship objects
    """
    return db.query(Relationship).filter(
        or_(
            Relationship.person_id == person_id,
            Relationship.related_person_id == person_id
        )
    ).all()


def get_relationship_by_type(
    db: Session, 
    person_id: UUID, 
    relationship_type: str
) -> List[Relationship]:
    """
    Get relationships of a specific type for a person.
    
    Args:
        db: Database session
        person_id: UUID of the person
        relationship_type: Type of relationship to filter
        
    Returns:
        List of Relationship objects
    """
    return db.query(Relationship).filter(
        Relationship.person_id == person_id,
        Relationship.relationship_type == relationship_type
    ).all()


def get_specific_relationship(
    db: Session,
    person_id: UUID,
    related_person_id: UUID,
    relationship_type: str
) -> Optional[Relationship]:
    """
    Check if a specific relationship exists.
    
    Args:
        db: Database session
        person_id: UUID of the primary person
        related_person_id: UUID of the related person
        relationship_type: Type of relationship
        
    Returns:
        Relationship object if found, None otherwise
    """
    return db.query(Relationship).filter(
        Relationship.person_id == person_id,
        Relationship.related_person_id == related_person_id,
        Relationship.relationship_type == relationship_type
    ).first()


def delete_relationship(db: Session, relationship_id: UUID) -> bool:
    """
    Delete a relationship from the database.
    
    Args:
        db: Database session
        relationship_id: UUID of the relationship to delete
        
    Returns:
        True if deleted, False if not found
    """
    relationship = get_relationship_by_id(db, relationship_id)
    if relationship:
        db.delete(relationship)
        db.commit()
        return True
    return False


def delete_relationship_by_persons(
    db: Session,
    person_id: UUID,
    related_person_id: UUID
) -> bool:
    """
    Delete all relationships between two persons.
    
    Args:
        db: Database session
        person_id: UUID of the first person
        related_person_id: UUID of the second person
        
    Returns:
        True if any deleted, False otherwise
    """
    result = db.query(Relationship).filter(
        or_(
            (Relationship.person_id == person_id) & 
            (Relationship.related_person_id == related_person_id),
            (Relationship.person_id == related_person_id) & 
            (Relationship.related_person_id == person_id)
        )
    ).delete()
    db.commit()
    return result > 0


def get_all_relationships(db: Session, skip: int = 0, limit: int = 100) -> List[Relationship]:
    """
    Get all relationships with pagination.
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        
    Returns:
        List of Relationship objects
    """
    return db.query(Relationship).offset(skip).limit(limit).all()


def get_relationship_by_id_and_tree(db: Session, relationship_id: UUID, tree_id: UUID) -> Optional[Relationship]:
    """
    Retrieve a relationship by ID, only if it belongs to the specified tree.
    
    Args:
        db: Database session
        relationship_id: UUID of the relationship
        tree_id: UUID of the tree
        
    Returns:
        Relationship object if found and belongs to tree, None otherwise
    """
    return db.query(Relationship).filter(
        Relationship.id == relationship_id,
        Relationship.tree_id == tree_id
    ).first()


def get_relationships_by_tree(db: Session, tree_id: UUID, skip: int = 0, limit: int = 100) -> List[Relationship]:
    """
    Get all relationships belonging to a specific tree.
    
    Args:
        db: Database session
        tree_id: UUID of the tree
        skip: Number of records to skip
        limit: Maximum number of records to return
        
    Returns:
        List of Relationship objects belonging to the tree
    """
    return db.query(Relationship).filter(Relationship.tree_id == tree_id).offset(skip).limit(limit).all()
