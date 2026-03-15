import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from app.core.database import Base


class User(Base):
    """
    User model for authentication and authorization.
    
    Roles:
    - SUPER_ADMIN: Can create FAMILY_ADMINs, see all users
    - FAMILY_ADMIN: Owns a tree, can create members/viewers for their tree
    - member: Can create/edit data in their tree
    - viewer: Read-only access to their tree
    """
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    mobile = Column(String(20), unique=True, nullable=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False)  # SUPER_ADMIN / FAMILY_ADMIN / member / viewer
    
    # Tree association - which tree this user belongs to
    tree_id = Column(UUID(as_uuid=True), ForeignKey("family_trees.id"), nullable=True)
    
    # Optional: link user to a person in the tree
    person_id = Column(UUID(as_uuid=True), ForeignKey("persons.id"), nullable=True)
    
    # Deprecated: use tree_id instead
    family_root_id = Column(UUID(as_uuid=True), ForeignKey("persons.id"), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)