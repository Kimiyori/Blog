from fastapi import Depends, Form, UploadFile
from src.utils.auth import (
    get_password_hash,
    oauth2_scheme,
    decode_token,
)
from src.utils.images import (
    save_user_image,
    get_user_image_filename,
    get_user_avatar_path,
)
import src.exceptions as exc
from src.db.schemas.user import UserOut, UserIn, UserCreate, UserUpdate
from src.unit_of_work import uow_context_manager, MongoDBUnitOfWork
from src.repository.user import UserRepository


async def create_new_user(
    user_data: UserIn,
    uow: MongoDBUnitOfWork[UserRepository] = Depends(
        uow_context_manager(UserRepository)
    ),
) -> UserOut:
    query = [
        {field: data}
        for field in ["username", "email"]
        if (data := getattr(user_data, field)) is not None
    ]
    if await uow.repo.count({"$or": query}):
        raise exc.UserExist()
    user_create = UserCreate(
        username=user_data.username,
        password=get_password_hash(user_data.password),
        email=user_data.email,
    )
    created_id = await uow.repo.add(user_create.dict())
    await uow.commit()
    assert (new_user := await uow.repo.get_by_id(created_id))
    return UserOut(**new_user)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    uow: MongoDBUnitOfWork[UserRepository] = Depends(
        uow_context_manager(UserRepository)
    ),
) -> UserOut:
    username = decode_token(token)
    if (user := await uow.repo.get_by_name(username)) is None:
        raise exc.UserNotExist()
    return UserOut(**user)


async def get_user_service(
    username: str,
    uow: MongoDBUnitOfWork[UserRepository] = Depends(
        uow_context_manager(UserRepository)
    ),
) -> UserOut:
    if (user := await uow.repo.get_by_name(username)) is None:
        raise exc.UserNotExist()
    return UserOut(**user)


async def update_user_service(
    username: str,
    image: UploadFile | None = None,
    email: str = Form(None),
    password: str = Form(None),
    user: UserOut = Depends(get_current_user),
    uow: MongoDBUnitOfWork[UserRepository] = Depends(
        uow_context_manager(UserRepository)
    ),
) -> UserUpdate:
    if user.username != username:
        raise exc.UserNotExist()
    filename = get_user_image_filename(image)
    upd_obj = UserUpdate(
        email=email if email else None,
        image=get_user_avatar_path(user.username) + "/" + filename
        if filename
        else None,
        password=get_password_hash(password) if password else None,
    )
    updated_data = await uow.repo.update_user(user.id, upd_obj)
    if image:
        save_user_image(image, filename, user.username)
    return UserUpdate(**updated_data)
