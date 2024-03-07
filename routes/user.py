from fastapi import APIRouter, HTTPException, Depends
from models.user import User
from schemas.user import UserCreate, UserInDB
from utils.auth import create_access_token
from tortoise.contrib.fastapi import HTTPNotFoundError
from utils.auth import get_password_hash

router = APIRouter()

@router.post("/register", response_model=UserInDB)
async def register_user(user: UserCreate):
    if await User.filter(username=user.username).exists():
        raise HTTPException(status_code=400, detail="Username already registered")
    
    password_hash = get_password_hash(user.password)  
    new_user = await User.create(username=user.username, password_hash=password_hash)
    return new_user
