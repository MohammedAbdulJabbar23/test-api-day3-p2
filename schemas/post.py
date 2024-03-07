from typing import List, Optional
from pydantic import BaseModel

class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    pass

class PostInDB(PostBase):
    id: int
    author: str

    class Config:
        orm_mode = True

class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    content: str
    post_id: int

class Comment(CommentBase):
    id: int

    class Config:
        orm_mode = True

class PostWithComments(BaseModel):
    id: int
    title: str
    content: str
    comments: List[Comment]

    class Config:
        orm_mode = True
