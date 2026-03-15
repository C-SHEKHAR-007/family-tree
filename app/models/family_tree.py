import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class FamilyTree(Base):
    """
    FamilyTree model represents a family tree entity.
    
    Each tree is owned by a FAMILY_ADMIN and contains:
    - Persons belonging to this tree
    - Users who have access to this tree (member, viewer roles)
    
    Tree isolation ensures users can only access their own tree's data.
    """
    __tablename__ = "family_trees"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    description = Column(String(500), nullable=True)
    
    # The FAMILY_ADMIN who owns this tree
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
