from fastapi import APIRouter, Depends, HTTPException, Response, status
from src.utils.auth import (
    create_access_token,
    create_refresh_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_MINUTES,
)
from src.service.user import (
    create_new_user,
    authenticate_user,
    get_current_user,
    refresh_token_service
)
from src.db.schemas.user import Token, UserIn, UserOut

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
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES,
        expires=ACCESS_TOKEN_EXPIRE_MINUTES,
    )
    response.set_cookie(
        key="refresh_token",
        value=f"Bearer {refresh_token}",
        max_age=REFRESH_TOKEN_EXPIRE_MINUTES,
        expires=REFRESH_TOKEN_EXPIRE_MINUTES,
    )
    return Token(access_token=access_token)


@router.post("/token", response_model=Token)
async def get_user_token(
    response: Response, user: UserIn = Depends(authenticate_user)
) -> Token:
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.username},
    )
    refresh_token = create_refresh_token(
        data={"sub": user.username},
    )
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES,
        expires=ACCESS_TOKEN_EXPIRE_MINUTES,
    )
    response.set_cookie(
        key="refresh_token",
        value=f"Bearer {refresh_token}",
        max_age=REFRESH_TOKEN_EXPIRE_MINUTES,
        expires=REFRESH_TOKEN_EXPIRE_MINUTES,
    )
    return Token(access_token=access_token)


@router.get(
    "/me", summary="Get details of currently logged in user", response_model=UserOut
)
async def read_users_me(current_user: UserOut = Depends(get_current_user)) -> UserOut:
    return current_user


@router.get(
    "/refresh",
    summary="Get details of currently logged in user",
    response_model=Token,
)
async def refresh_token(
    response: Response, access_token: str = Depends(refresh_token_service)
) -> Token:
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES,
        expires=ACCESS_TOKEN_EXPIRE_MINUTES,
    )
    return Token(access_token=access_token)

@router.get('/logout', status_code=status.HTTP_200_OK)
def logout(response: Response, current_user: UserOut = Depends(get_current_user)):
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    return {'status': 'success'}
    
