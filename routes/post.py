from fastapi import APIRouter, Depends, HTTPException
from models.post import Post
from schemas.post import PostCreate, PostInDB
from models.user import User
from schemas.user import UserInDB
from utils.auth import get_current_user
from tortoise.contrib.fastapi import HTTPNotFoundError

router = APIRouter()

@router.get("/posts/me")
async def read_posts_me(current_user: User = Depends(get_current_user)):
    return await Post.filter(author=current_user)

@router.post("/posts")
async def create_post(post: PostCreate, current_user: User = Depends(get_current_user)):
    new_post = await Post.create(**post.dict(exclude_unset=True), author=current_user)
    return new_post
