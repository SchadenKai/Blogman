from datetime import datetime
import hashlib
import uuid
from pydantic import EmailStr, field_validator
from typing import List, Optional

from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    username: str = Field(unique=True)
    fullname: str
    email: EmailStr = Field(unique=True)
    follower: int
    following: str

class UserCreate(UserBase):
    password: str = Field(min_length=8)
    @field_validator("fullname", mode="before")
    def capitalize_name(cls, value : str):
        return value.title()
    @field_validator("password", mode="after")
    def hash_password(cls, value: str) -> str:
        return hashlib.sha256(value.encode()).hexdigest()

class UserRead(UserBase):
    id: int

class UserUpdate(UserBase):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(min_length=8, default=None)
    updated_at: Optional[datetime] = datetime.now()

class UserDelete(UserBase):
    id: int
    
class UserLogin(UserBase):
    username: str
    password: str
    
    @field_validator("password", mode="after")
    def hash_password(cls, v : str):
        return hashlib.sha256(v.encode()).hexdigest()