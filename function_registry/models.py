import uuid
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class Function(Base):
    __tablename__ = "functions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False)
    image = Column(String, nullable=False)
    runtime = Column(String, nullable=False)
    is_warm = Column(Boolean, default=False)
    last_invoked_at = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())
