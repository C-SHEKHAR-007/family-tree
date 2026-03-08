import uuid
from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from app.core.database import Base

class Relationship(Base):
    __tablename__ = "relationships"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    person_id = Column(UUID(as_uuid=True), ForeignKey("persons.id"), nullable=False)
    related_person_id = Column(UUID(as_uuid=True), ForeignKey("persons.id"), nullable=False)
    relationship_type = Column(String(20), nullable=False)  # MOTHER / FATHER / SPOUSE / CHILD
    created_at = Column(DateTime, default=datetime.utcnow)