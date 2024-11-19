from datetime import datetime
from typing import List, Optional
import uuid

from sqlmodel import SQLModel
from sqlmodel import Field, Relationship
from api.blog.blog import BlogBase
from api.comment.schema import CommentBase
from user.schema import UserBase

class User(UserBase, table=True):
    id: Optional[uuid.UUID] = Field(primary_key=True, default_factory=uuid.uuid4)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    password: str
    
    blogs: List["Blog"] = Relationship(back_populates="owner", sa_relationship_kwargs={"cascade" : "all, delete"})
    comments: List["Comment"] = Relationship(back_populates="user", sa_relationship_kwargs={"cascade" : "all, delete"})

class Blog(BlogBase, table=True):
    id: Optional[int] = Field(primary_key=True)
    owner_id: Optional[uuid.UUID] = Field(foreign_key="user.id", nullable=False)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    
    owner: "User" = Relationship(back_populates="blogs")
    comments: List["Comment"] = Relationship(back_populates="blog")
    
    
class Comment(CommentBase, table=True):
    id: Optional[int] = Field(primary_key=True)
    user_id: Optional[uuid.UUID] = Field(foreign_key="user.id", nullable=False)
    blog_id: Optional[int] = Field(foreign_key="blog.id", nullable=False)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    
    user: User = Relationship(back_populates="comments")
    blog: Blog = Relationship(back_populates="comments")