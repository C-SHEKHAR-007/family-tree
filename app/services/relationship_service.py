#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
relationship_service.py - Business logic layer for Relationship operations.

Author: Family Tree API Team
Created: 2026-02-23

This module provides business logic for managing family relationships.

OWASP Secure Coding Practices:
    - Input validation
    - Proper error handling
    - Data integrity checks (prevent circular relationships)
"""

from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session

from app.repository import relationship_repo, person_repo
from app.schemas.relationship_schema import RelationshipCreate, FamilyRelationships


# Inverse relationship mapping for bidirectional relationships
INVERSE_RELATIONSHIPS = {
    "FATHER": "CHILD",
    "MOTHER": "CHILD",
    "CHILD": None,  # Don't auto-create parent from child
    "SPOUSE": "SPOUSE",
    "SIBLING": "SIBLING",
}


def create_relationship(db: Session, relationship_data: RelationshipCreate):
    """
    Create a family relationship between two persons.
    
    Validates that both persons exist and prevents self-referencing.
    Creates inverse relationships where applicable.
    
    Args:
        db: Database session
        relationship_data: Relationship creation data
        
    Returns:
        Created Relationship object
        
    Raises:
        ValueError: If validation fails
    """
    # Validate persons exist
    person = person_repo.get_person_by_id(db, relationship_data.person_id)
    if not person:
        raise ValueError(f"Person with id {relationship_data.person_id} not found")
    
    related_person = person_repo.get_person_by_id(db, relationship_data.related_person_id)
    if not related_person:
        raise ValueError(f"Related person with id {relationship_data.related_person_id} not found")
    
    # Prevent self-referencing
    if relationship_data.person_id == relationship_data.related_person_id:
        raise ValueError("Cannot create relationship with self")
    
    # Check if relationship already exists
    existing = relationship_repo.get_specific_relationship(
        db,
        relationship_data.person_id,
        relationship_data.related_person_id,
        relationship_data.relationship_type.value
    )
    if existing:
        raise ValueError("This relationship already exists")
    
    # Create the relationship
    rel_dict = {
        "person_id": relationship_data.person_id,
        "related_person_id": relationship_data.related_person_id,
        "relationship_type": relationship_data.relationship_type.value
    }
    relationship = relationship_repo.create_relationship(db, rel_dict)
    
    # Create inverse relationship if applicable
    inverse_type = INVERSE_RELATIONSHIPS.get(relationship_data.relationship_type.value)
    if inverse_type:
        # Check if inverse already exists
        inverse_existing = relationship_repo.get_specific_relationship(
            db,
            relationship_data.related_person_id,
            relationship_data.person_id,
            inverse_type
        )
        if not inverse_existing:
            inverse_dict = {
                "person_id": relationship_data.related_person_id,
                "related_person_id": relationship_data.person_id,
                "relationship_type": inverse_type
            }
            relationship_repo.create_relationship(db, inverse_dict)
    
    return relationship


def get_relationship_by_id(db: Session, relationship_id: UUID):
    """
    Get a relationship by ID.
    
    Args:
        db: Database session
        relationship_id: UUID of the relationship
        
    Returns:
        Relationship object
        
    Raises:
        ValueError: If relationship not found
    """
    relationship = relationship_repo.get_relationship_by_id(db, relationship_id)
    if not relationship:
        raise ValueError(f"Relationship with id {relationship_id} not found")
    return relationship


def get_relationships_for_person(db: Session, person_id: UUID) -> List:
    """
    Get all relationships for a person.
    
    Args:
        db: Database session
        person_id: UUID of the person
        
    Returns:
        List of Relationship objects
    """
    # Verify person exists
    person = person_repo.get_person_by_id(db, person_id)
    if not person:
        raise ValueError(f"Person with id {person_id} not found")
    
    return relationship_repo.get_relationships_by_person(db, person_id)


def get_family_relationships(db: Session, person_id: UUID) -> FamilyRelationships:
    """
    Get organized family relationships for a person.
    
    Args:
        db: Database session
        person_id: UUID of the person
        
    Returns:
        FamilyRelationships object with categorized relations
    """
    # Verify person exists
    person = person_repo.get_person_by_id(db, person_id)
    if not person:
        raise ValueError(f"Person with id {person_id} not found")
    
    relationships = relationship_repo.get_relationships_by_person(db, person_id)
    
    result = FamilyRelationships(person_id=person_id)
    
    for rel in relationships:
        if rel.person_id == person_id:
            # Relationships where this person is the subject
            if rel.relationship_type == "FATHER":
                result.father = rel.related_person_id
            elif rel.relationship_type == "MOTHER":
                result.mother = rel.related_person_id
            elif rel.relationship_type == "SPOUSE":
                result.spouse = rel.related_person_id
            elif rel.relationship_type == "CHILD":
                result.children.append(rel.related_person_id)
            elif rel.relationship_type == "SIBLING":
                if rel.related_person_id not in result.siblings:
                    result.siblings.append(rel.related_person_id)
    
    return result


def delete_relationship(db: Session, relationship_id: UUID) -> bool:
    """
    Delete a relationship.
    
    Args:
        db: Database session
        relationship_id: UUID of the relationship to delete
        
    Returns:
        True if deleted
        
    Raises:
        ValueError: If relationship not found
    """
    existing = relationship_repo.get_relationship_by_id(db, relationship_id)
    if not existing:
        raise ValueError(f"Relationship with id {relationship_id} not found")
    
    return relationship_repo.delete_relationship(db, relationship_id)


def delete_relationships_between_persons(
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
        True if any relationships were deleted
    """
    return relationship_repo.delete_relationship_by_persons(
        db, person_id, related_person_id
    )


def get_all_relationships(db: Session, skip: int = 0, limit: int = 100) -> List:
    """
    Get all relationships with pagination.
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        
    Returns:
        List of Relationship objects
    """
    return relationship_repo.get_all_relationships(db, skip, limit)
