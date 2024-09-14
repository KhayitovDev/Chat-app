from sqlalchemy import Column, String, ForeignKey, Text, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from uuid import uuid4

from app.db.database import Base
from app.services.schemas import UserRoles

class User(Base):
    __tablename__ = "users"
    id = Column(UUID, primary_key=True, default=uuid4)
    username = Column(String, unique=True, index=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    preferred_language = Column(String) 
    hashed_password = Column(String) 
    status = Column(Enum(UserRoles), default=UserRoles.MEMBER)
    