from typing import List, Optional
from pydantic import BaseModel, validator

from uuid import UUID
from enum import Enum


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
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    preferred_language: Optional[str] = None
    status: Optional[UserRoles] = UserRoles.MEMBER
    
    @validator("preferred_language")
    def validate_language(cls, value):
        if len(value) != 2 or not value.isalpha():
            raise ValueError("preferred_language must be a two-letter language code.")
        return value.lower()
    
    
    

    
    