from fastapi import APIRouter, Depends, Response, status
from src.utils.auth import (
    create_access_token,
    create_refresh_token,
    set_cookie,
)
from src.service.user import (
    create_new_user,
    get_current_user,
    get_user_service,
    update_user_service,
)
from src.db.schemas.user import Token, UserIn, UserOut, UserUpdate

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(
    response: Response, user: UserIn = Depends(create_new_user)
) -> Token:
    access_token = create_access_token(
        data={"sub": user.username},
    )
    refresh_token = create_refresh_token(
        data={"sub": user.username},
    )
    set_cookie(response, access_token, refresh_token)
    return Token(access_token=access_token)


@router.get(
    "/me", summary="Get details of currently logged in user", response_model=UserOut
)
async def read_users_me(current_user: UserOut = Depends(get_current_user)) -> UserOut:
    return current_user


@router.get(
    "/{username}",
    response_model=UserOut,
)
async def get_user(user: UserOut = Depends(get_user_service)) -> UserOut:
    return user


@router.patch(
    "",
)
async def put_user(
    updated_data: UserUpdate = Depends(update_user_service),
) -> UserUpdate:
    return updated_data
