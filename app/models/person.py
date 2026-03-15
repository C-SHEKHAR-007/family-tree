import uuid
from sqlalchemy import Column, String, Date, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from app.core.database import Base


class Person(Base):
    """
    Person model represents a family member in a tree.
    
    Each person belongs to exactly one tree (tree_id).
    This ensures data isolation between different family trees.
    """
    __tablename__ = "persons"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    gender = Column(String(10), nullable=False)
    date_of_birth = Column(Date, nullable=True)
    mobile = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    birth_place = Column(String(255), nullable=True)
    
    # Tree association - which tree this person belongs to
    tree_id = Column(UUID(as_uuid=True), ForeignKey("family_trees.id"), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)