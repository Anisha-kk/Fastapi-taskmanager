from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, Enum as SQLEnum, ForeignKey
)
from app.schemas.task import StatusEnum,PriorityEnum
from app.db.session import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)

    # New fields based on schema
    status = Column(SQLEnum(StatusEnum), default=StatusEnum.pending, nullable=False)
    priority = Column(SQLEnum(PriorityEnum), default=PriorityEnum.medium, nullable=False)
    due_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=True)

    # Relationships
    ownername = Column(String, ForeignKey("users.username"), nullable=False)
    owner = relationship("User", backref="tasks")