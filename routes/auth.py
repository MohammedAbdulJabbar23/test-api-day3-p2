from fastapi import APIRouter, Depends, HTTPException
from utils.auth import create_access_token, authenticate_user, get_current_user
from models.user import User
from schemas.user import UserCreate, Token

router = APIRouter()

@router.post("/login", response_model=Token)
async def login_for_access_token(user: UserCreate):
    db_user = await authenticate_user(user.username, user.password)
    if not db_user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token({"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
