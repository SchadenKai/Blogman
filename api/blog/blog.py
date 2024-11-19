from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel

class BlogBase(SQLModel):
    title: str
    content: str
    upvote: int = 0
    downvote: int = 0

class BlogCreate(BlogBase):
    pass

class BlogRead(BlogBase):
    id: int
    owner_id: int

class BlogUpdate(BlogBase):
    title: Optional[str] = None
    content: Optional[str] = None
    updated_at: Optional[datetime] = datetime.now()

    
class PublicBlogUpdate(BlogBase):
    upvote: Optional[int] = None
    downvote: Optional[int] = None

class BlogDelete(BlogBase):
    id: int