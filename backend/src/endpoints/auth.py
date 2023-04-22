from fastapi import APIRouter, Depends, Response, status
from src.utils.auth import (
    create_access_token,
    create_refresh_token,
    set_cookie,
)
from src.service.user import get_current_user
from src.service.auth import authenticate_user, refresh_token_check
from src.db.schemas.user import Token, UserIn, UserOut

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/token", response_model=Token)
async def get_user_token(
    response: Response, user: UserIn = Depends(authenticate_user)
) -> Token:
    access_token = create_access_token(
        data={"sub": user.username},
    )
    refresh_token = create_refresh_token(
        data={"sub": user.username},
    )
    set_cookie(response, access_token, refresh_token, True)
    return Token(access_token=access_token)


@router.get(
    "/refresh",
    response_model=Token,
)
async def refresh_token(
    response: Response, user: UserOut = Depends(refresh_token_check)
) -> Token:
    access_token = create_access_token(
        data={"sub": user.username},
    )
    refresh_token = create_refresh_token(
        data={"sub": user.username},
    )
    set_cookie(response, access_token, refresh_token, True)
    return Token(access_token=access_token)


@router.get("/logout", status_code=status.HTTP_200_OK)
def logout(
    response: Response, current_user: UserOut = Depends(get_current_user)
) -> dict[str, str]:
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    response.set_cookie(key="logged_in", value="", max_age=-1)
    return {"status": "success"}
