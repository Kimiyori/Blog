from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from src.utils.auth import (
    require_refresh_token,
    verify_password,
    decode_refresh_token,
)
import src.exceptions as exc
from src.db.schemas.user import UserOut, UserIn
from src.unit_of_work import uow_context_manager, MongoDBUnitOfWork
from src.repository.user import UserRepository


async def authenticate_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    uow: MongoDBUnitOfWork[UserRepository] = Depends(
        uow_context_manager(UserRepository)
    ),
) -> UserIn | bool:
    if (user := await uow.repo.get_by_name(form_data.username)) is None:
        raise exc.UserNotExist()
    if not verify_password(form_data.password, user["password"]):
        raise exc.ValidateCredentials()
    return UserIn(**user)


async def refresh_token_check(
    token: str = Depends(require_refresh_token),
    uow: MongoDBUnitOfWork[UserRepository] = Depends(
        uow_context_manager(UserRepository)
    ),
) -> UserOut:
    username = decode_refresh_token(token)
    if (user := await uow.repo.get_by_name(username)) is None:
        raise exc.UserNotExist()
    return UserOut(**user)
