from typing import List, Optional
from pydantic import BaseModel, field_validator

from sqlalchemy import Text

from uuid import UUID
from enum import Enum



class UserLogin(BaseModel):
    username: str
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    username: str

class UserRoles(str, Enum):
    ADMIN = "admin"
    MEMBER = "member"
    
class UserBase(BaseModel):
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    preferred_language: Optional[str] = None
    
class UserCreate(UserBase):
    username: str
    hashed_password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    preferred_language: Optional[str] = None
    status: Optional[UserRoles] = UserRoles.MEMBER
    
    # @field_validator("preferred_language")
    # def validate_language(cls, value):
    #     if value and (len(value) != 4 or not value.isalpha()):
    #         raise ValueError("preferred_language must be a two-letter language code.")
    #     return value.lower() if value else value
      
class UserResponse(UserBase):
    id: UUID
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    status: UserRoles
    
class InvitationStatus(Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    
class InvitationStatusUpdate(BaseModel):
    status: InvitationStatus
    
class InvitationCreate(BaseModel):
    sender_id: UUID
    receiver_id: UUID
    status: Optional[InvitationStatus] = InvitationStatus.PENDING
    

class MessageCreate(BaseModel):
    sender_id: UUID
    receiver_id: UUID
    content: str
    
    
    
    
    
    