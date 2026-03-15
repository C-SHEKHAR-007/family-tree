#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tree_service.py - Business logic layer for Family Tree operations.

Author: Family Tree API Team
Created: 2026-02-23

This module provides business logic for family tree traversal and queries.

OWASP Secure Coding Practices:
    - Input validation
    - Proper error handling
    - Prevention of infinite recursion
"""

from typing import List, Dict, Any, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from app.repository import person_repo, relationship_repo
from app.models.person import Person
from app.models.relationship import Relationship


MAX_RECURSION_DEPTH = 10  # Prevent infinite loops


def get_ancestors(
    db: Session, 
    person_id: UUID, 
    max_depth: int = MAX_RECURSION_DEPTH,
    tree_id: UUID = None
) -> List[Dict[str, Any]]:
    """
    Get all ancestors of a person (parents, grandparents, etc.).
    
    Uses recursive traversal with depth limit.
    
    Args:
        db: Database session
        person_id: UUID of the person
        max_depth: Maximum recursion depth
        tree_id: Optional UUID of the tree (for access control)
        
    Returns:
        List of ancestor dictionaries with person info and generation level
        
    Raises:
        ValueError: If person not found or not in user's tree
    """
    if tree_id:
        person = person_repo.get_person_by_id_and_tree(db, person_id, tree_id)
        if not person:
            raise ValueError(f"Person with id {person_id} not found in your tree")
    else:
        person = person_repo.get_person_by_id(db, person_id)
        if not person:
            raise ValueError(f"Person with id {person_id} not found")
    
    ancestors = []
    visited = set()
    
    def _traverse_ancestors(p_id: UUID, generation: int):
        if generation > max_depth or p_id in visited:
            return
        
        visited.add(p_id)
        
        # Get parent relationships
        parent_rels = relationship_repo.get_relationship_by_type(db, p_id, "FATHER")
        parent_rels.extend(relationship_repo.get_relationship_by_type(db, p_id, "MOTHER"))
        
        for rel in parent_rels:
            parent = person_repo.get_person_by_id(db, rel.related_person_id)
            if parent:
                ancestors.append({
                    "id": str(parent.id),
                    "first_name": parent.first_name,
                    "last_name": parent.last_name,
                    "gender": parent.gender,
                    "relationship_type": rel.relationship_type,
                    "generation": generation,
                })
                _traverse_ancestors(parent.id, generation + 1)
    
    _traverse_ancestors(person_id, 1)
    return ancestors


def get_descendants(
    db: Session, 
    person_id: UUID, 
    max_depth: int = MAX_RECURSION_DEPTH,
    tree_id: UUID = None
) -> List[Dict[str, Any]]:
    """
    Get all descendants of a person (children, grandchildren, etc.).
    
    Uses recursive traversal with depth limit.
    
    Args:
        db: Database session
        person_id: UUID of the person
        max_depth: Maximum recursion depth
        tree_id: Optional UUID of the tree (for access control)
        
    Returns:
        List of descendant dictionaries with person info and generation level
        
    Raises:
        ValueError: If person not found or not in user's tree
    """
    if tree_id:
        person = person_repo.get_person_by_id_and_tree(db, person_id, tree_id)
        if not person:
            raise ValueError(f"Person with id {person_id} not found in your tree")
    else:
        person = person_repo.get_person_by_id(db, person_id)
        if not person:
            raise ValueError(f"Person with id {person_id} not found")
    
    descendants = []
    visited = set()
    
    def _traverse_descendants(p_id: UUID, generation: int):
        if generation > max_depth or p_id in visited:
            return
        
        visited.add(p_id)
        
        # Get child relationships
        child_rels = relationship_repo.get_relationship_by_type(db, p_id, "CHILD")
        
        for rel in child_rels:
            child = person_repo.get_person_by_id(db, rel.related_person_id)
            if child:
                descendants.append({
                    "id": str(child.id),
                    "first_name": child.first_name,
                    "last_name": child.last_name,
                    "gender": child.gender,
                    "generation": generation,
                })
                _traverse_descendants(child.id, generation + 1)
    
    _traverse_descendants(person_id, 1)
    return descendants


def get_siblings(db: Session, person_id: UUID, tree_id: UUID = None) -> List[Dict[str, Any]]:
    """
    Get all siblings of a person.
    
    Siblings are derived from shared parents or direct sibling relationships.
    
    Args:
        db: Database session
        person_id: UUID of the person
        tree_id: Optional UUID of the tree (for access control)
        
    Returns:
        List of sibling dictionaries
        
    Raises:
        ValueError: If person not found or not in user's tree
    """
    if tree_id:
        person = person_repo.get_person_by_id_and_tree(db, person_id, tree_id)
        if not person:
            raise ValueError(f"Person with id {person_id} not found in your tree")
    else:
        person = person_repo.get_person_by_id(db, person_id)
        if not person:
            raise ValueError(f"Person with id {person_id} not found")
    
    siblings = []
    sibling_ids = set()
    
    # Get direct sibling relationships
    sibling_rels = relationship_repo.get_relationship_by_type(db, person_id, "SIBLING")
    for rel in sibling_rels:
        if rel.related_person_id not in sibling_ids:
            sibling_ids.add(rel.related_person_id)
            sibling = person_repo.get_person_by_id(db, rel.related_person_id)
            if sibling:
                siblings.append({
                    "id": str(sibling.id),
                    "first_name": sibling.first_name,
                    "last_name": sibling.last_name,
                    "gender": sibling.gender,
                })
    
    # Also derive siblings from shared parents
    parent_rels = relationship_repo.get_relationship_by_type(db, person_id, "FATHER")
    parent_rels.extend(relationship_repo.get_relationship_by_type(db, person_id, "MOTHER"))
    
    for parent_rel in parent_rels:
        # Get all children of this parent
        parent_children = relationship_repo.get_relationship_by_type(
            db, parent_rel.related_person_id, "CHILD"
        )
        for child_rel in parent_children:
            child_id = child_rel.related_person_id
            if child_id != person_id and child_id not in sibling_ids:
                sibling_ids.add(child_id)
                sibling = person_repo.get_person_by_id(db, child_id)
                if sibling:
                    siblings.append({
                        "id": str(sibling.id),
                        "first_name": sibling.first_name,
                        "last_name": sibling.last_name,
                        "gender": sibling.gender,
                    })
    
    return siblings


def build_family_tree(
    db: Session, 
    root_person_id: UUID, 
    depth: int = 3,
    tree_id: UUID = None
) -> Dict[str, Any]:
    """
    Build a complete family tree structure starting from a person.
    
    Args:
        db: Database session
        root_person_id: UUID of the root person
        depth: How many generations to include
        tree_id: Optional UUID of the tree (for access control)
        
    Returns:
        Dictionary representing the family tree structure
        
    Raises:
        ValueError: If person not found or not in user's tree
    """
    if tree_id:
        person = person_repo.get_person_by_id_and_tree(db, root_person_id, tree_id)
        if not person:
            raise ValueError(f"Person with id {root_person_id} not found in your tree")
    else:
        person = person_repo.get_person_by_id(db, root_person_id)
        if not person:
            raise ValueError(f"Person with id {root_person_id} not found")
    
    def _build_node(p_id: UUID, current_depth: int) -> Optional[Dict[str, Any]]:
        if current_depth > depth:
            return None
        
        p = person_repo.get_person_by_id(db, p_id)
        if not p:
            return None
        
        node = {
            "id": str(p.id),
            "first_name": p.first_name,
            "last_name": p.last_name,
            "gender": p.gender,
            "date_of_birth": str(p.date_of_birth) if p.date_of_birth else None,
            "children": [],
            "spouse": None,
        }
        
        # Get spouse
        spouse_rels = relationship_repo.get_relationship_by_type(db, p_id, "SPOUSE")
        if spouse_rels:
            spouse = person_repo.get_person_by_id(db, spouse_rels[0].related_person_id)
            if spouse:
                node["spouse"] = {
                    "id": str(spouse.id),
                    "first_name": spouse.first_name,
                    "last_name": spouse.last_name,
                    "gender": spouse.gender,
                }
        
        # Get children recursively
        child_rels = relationship_repo.get_relationship_by_type(db, p_id, "CHILD")
        for child_rel in child_rels:
            child_node = _build_node(child_rel.related_person_id, current_depth + 1)
            if child_node:
                node["children"].append(child_node)
        
        return node
    
    return _build_node(root_person_id, 1)


def get_tree_statistics(db: Session, root_person_id: UUID, tree_id: UUID = None) -> Dict[str, Any]:
    """
    Get statistics about a family tree.
    
    Args:
        db: Database session
        root_person_id: UUID of the root person
        tree_id: Optional UUID of the tree (for access control)
        
    Returns:
        Dictionary with tree statistics
        
    Raises:
        ValueError: If person not found or not in user's tree
    """
    if tree_id:
        person = person_repo.get_person_by_id_and_tree(db, root_person_id, tree_id)
        if not person:
            raise ValueError(f"Person with id {root_person_id} not found in your tree")
    else:
        person = person_repo.get_person_by_id(db, root_person_id)
        if not person:
            raise ValueError(f"Person with id {root_person_id} not found")
    
    ancestors = get_ancestors(db, root_person_id, tree_id=tree_id)
    descendants = get_descendants(db, root_person_id, tree_id=tree_id)
    siblings = get_siblings(db, root_person_id, tree_id=tree_id)
    
    # Calculate max generation depth
    ancestor_generations = max([a["generation"] for a in ancestors], default=0)
    descendant_generations = max([d["generation"] for d in descendants], default=0)
    
    return {
        "root_person_id": str(root_person_id),
        "root_person_name": f"{person.first_name} {person.last_name}",
        "total_ancestors": len(ancestors),
        "total_descendants": len(descendants),
        "total_siblings": len(siblings),
        "ancestor_generations": ancestor_generations,
        "descendant_generations": descendant_generations,
        "total_family_members": len(ancestors) + len(descendants) + len(siblings) + 1,
    }
