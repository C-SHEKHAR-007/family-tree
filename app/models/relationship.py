import uuid
from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from app.core.database import Base


class Relationship(Base):
    """
    Relationship model represents a family relationship between two persons.
    
    Each relationship belongs to a tree (tree_id) for data isolation.
    """
    __tablename__ = "relationships"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    person_id = Column(UUID(as_uuid=True), ForeignKey("persons.id"), nullable=False)
    related_person_id = Column(UUID(as_uuid=True), ForeignKey("persons.id"), nullable=False)
    relationship_type = Column(String(20), nullable=False)  # MOTHER / FATHER / SPOUSE / CHILD
    
    # Tree association - which tree this relationship belongs to
    tree_id = Column(UUID(as_uuid=True), ForeignKey("family_trees.id"), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)