#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
family_tree_repo.py - Repository layer for FamilyTree database operations.

Author: Family Tree API Team
Created: 2026-03-15

This module provides database access functions for FamilyTree model.
"""

from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session
from app.models.family_tree import FamilyTree


def create_tree(db: Session, tree_data: dict) -> FamilyTree:
    """
    Create a new family tree in the database.
    
    Args:
        db: Database session
        tree_data: Dictionary containing tree fields
        
    Returns:
        Created FamilyTree object
    """
    tree = FamilyTree(**tree_data)
    db.add(tree)
    db.commit()
    db.refresh(tree)
    return tree


def get_tree_by_id(db: Session, tree_id: UUID) -> Optional[FamilyTree]:
    """
    Retrieve a family tree by ID.
    
    Args:
        db: Database session
        tree_id: UUID of the tree
        
    Returns:
        FamilyTree object if found, None otherwise
    """
    return db.query(FamilyTree).filter(FamilyTree.id == tree_id).first()


def get_tree_by_owner(db: Session, owner_id: UUID) -> Optional[FamilyTree]:
    """
    Retrieve a family tree by owner ID.
    
    Args:
        db: Database session
        owner_id: UUID of the tree owner
        
    Returns:
        FamilyTree object if found, None otherwise
    """
    return db.query(FamilyTree).filter(FamilyTree.owner_id == owner_id).first()


def get_all_trees(db: Session, skip: int = 0, limit: int = 100) -> List[FamilyTree]:
    """
    Retrieve all family trees with pagination (for SUPER_ADMIN).
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        
    Returns:
        List of FamilyTree objects
    """
    return db.query(FamilyTree).offset(skip).limit(limit).all()


def update_tree(db: Session, tree_id: UUID, tree_data: dict) -> Optional[FamilyTree]:
    """
    Update an existing family tree.
    
    Args:
        db: Database session
        tree_id: UUID of the tree to update
        tree_data: Dictionary containing fields to update
        
    Returns:
        Updated FamilyTree object if found, None otherwise
    """
    tree = db.query(FamilyTree).filter(FamilyTree.id == tree_id).first()
    if tree:
        for key, value in tree_data.items():
            if hasattr(tree, key) and value is not None:
                setattr(tree, key, value)
        db.commit()
        db.refresh(tree)
    return tree


def delete_tree(db: Session, tree_id: UUID) -> bool:
    """
    Delete a family tree.
    
    Args:
        db: Database session
        tree_id: UUID of the tree to delete
        
    Returns:
        True if deleted, False if not found
    """
    tree = db.query(FamilyTree).filter(FamilyTree.id == tree_id).first()
    if tree:
        db.delete(tree)
        db.commit()
        return True
    return False
