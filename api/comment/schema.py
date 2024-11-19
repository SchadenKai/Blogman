from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel

class CommentBase(SQLModel):
    content: str
    blog_id: int

class CommentCreate(CommentBase):
    pass

class CommentRead(CommentBase):
    id: int
    user_id: int

class CommentUpdate(CommentBase):
    content: Optional[str] = None
    updated_at: Optional[datetime] = datetime.now()

class CommentDelete(CommentBase):
    id: int