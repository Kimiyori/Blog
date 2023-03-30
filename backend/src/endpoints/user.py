from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from src.service.user import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    create_new_user,
    authenticate_user,
    get_current_user,
)
from src.db.schemas.user import Token, UserIn, UserOut

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserIn = Depends(create_new_user)) -> Token:
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return Token(access_token=access_token, token_type="bearer")


@router.post("/token", response_model=Token)
async def get_user_token(user: UserIn = Depends(authenticate_user)) -> Token:
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get(
    "/me", summary="Get details of currently logged in user", response_model=UserOut
)
async def read_users_me(current_user: UserOut = Depends(get_current_user)) -> UserOut:
    return current_user
