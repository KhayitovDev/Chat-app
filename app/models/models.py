from sqlalchemy import Column, String, ForeignKey, Text, Enum, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from uuid import uuid4
from datetime import datetime

from app.db.database import Base
from app.services.schemas import UserRoles, InvitationStatus

class User(Base):
    __tablename__ = "users"
    id = Column(UUID, primary_key=True, default=uuid4)
    username = Column(String, unique=True, index=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    preferred_language = Column(String) 
    hashed_password = Column(String) 
    status = Column(Enum(UserRoles), default=UserRoles.MEMBER)
    
    sent_invitations = relationship("Invitation", foreign_keys="Invitation.sender_id", back_populates="sender")
    received_invitations = relationship("Invitation", foreign_keys="Invitation.receiver_id", back_populates="receiver")
    sent_messages = relationship("Message", foreign_keys="Message.sender_id", back_populates="sender")
    received_messages = relationship("Message", foreign_keys="Message.receiver_id", back_populates="receiver")

class Invitation(Base):
    __tablename__= "invitations"
    id = Column(UUID, primary_key=True, default=uuid4)
    sender_id = Column(UUID, ForeignKey("users.id"), nullable=False)
    receiver_id = Column(UUID, ForeignKey("users.id"), nullable=False)
    status = Column(Enum(InvitationStatus), default=InvitationStatus.PENDING)
    
    sender = relationship("User", foreign_keys=[sender_id], back_populates="sent_invitations")
    receiver = relationship("User", foreign_keys=[receiver_id], back_populates="received_invitations")
    
class Message(Base):
    __tablename__ = "messages"
    id = Column(UUID, primary_key=True, default=uuid4)
    content = Column(Text, nullable=False)
    sender_id = Column(UUID, ForeignKey('users.id'), nullable=False)
    receiver_id = Column(UUID, ForeignKey('users.id'), nullable=False)
    
    sender = relationship("User", foreign_keys=[sender_id], back_populates="sent_messages")
    receiver = relationship("User", foreign_keys=[receiver_id], back_populates="received_messages")
    
    
