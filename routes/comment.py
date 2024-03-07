from fastapi import APIRouter, Depends, HTTPException
from typing import List
from tortoise.contrib.fastapi import HTTPNotFoundError
from models.post import Post 
from models.comment import Comment 
from models.user import User 
from schemas.user import UserCreate
from schemas.post import CommentCreate, PostCreate, Comment as CommentSchema, PostWithComments
from utils.auth import get_current_user

router = APIRouter()

@router.get("/user/posts-with-comments", response_model=List[PostWithComments])
async def get_user_posts_with_comments(current_user: User = Depends(get_current_user)):
    user_posts = await Post.filter(author=current_user).prefetch_related("comments")
    posts_with_comments = []
    for post in user_posts:
        post_data = {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "author": post.author,
            "comments": [comment.dict() for comment in post.comments]
        }
        posts_with_comments.append(post_data)
    return posts_with_comments



@router.post("/comments/", response_model=CommentSchema)
async def create_comment(
    comment: CommentCreate, current_user: User = Depends(get_current_user)
):
    comment_data = comment.dict()
    comment_data["author_id"] = current_user.id  

    new_comment = await Comment.create(**comment_data)
    
    return new_comment

@router.get("/posts-with-comments/{user_id}", response_model=List[PostWithComments])
async def get_user_posts_with_comments(user_id: int):
    user_posts = await Post.filter(author_id=user_id).prefetch_related("comments")
    posts_with_comments = []
    for post in user_posts:
        comments = []
        for comment in post.comments:
            comments.append({
                "id": comment.id,
                "text": comment.text,
                "user_id": comment.user_id
            })
        posts_with_comments.append({
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "comments": comments  
        })
    return posts_with_comments




@router.get("/comments/", response_model=List[CommentSchema])
async def read_comments():
    return await CommentSchema.from_queryset(Comment.all())

@router.get("/comments/{comment_id}/", response_model=CommentSchema)
async def read_comment(comment_id: int):
    return await CommentSchema.from_queryset_single(Comment.get(id=comment_id))

@router.put("/comments/{comment_id}/", response_model=CommentSchema)
async def update_comment(comment_id: int, comment: CommentCreate):
    await Comment.filter(id=comment_id).update(**comment.dict(exclude_unset=True))
    return await CommentSchema.from_queryset_single(Comment.get(id=comment_id))

@router.delete("/comments/{comment_id}/", response_model=dict)
async def delete_comment(comment_id: int):
    deleted_count = await Comment.filter(id=comment_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail="Comment not found")
    return {"message": "Comment deleted successfully"}