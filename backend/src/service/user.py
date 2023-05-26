import base64
import json
from fastapi import Depends
from pydantic import BaseModel
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
from src.db.schemas.user import (
    UserOut,
    UserIn,
    UserCreate,
    UserUpdate,
    UserUpdateResponse,
)
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
    if (user := await uow.repo.get_by_name(username, return_password=False)) is None:
        raise exc.UserNotExist()
    return UserOut(
        username=user["username"],
        email=user["email"],
        _id=user["_id"],
        created_at=user["created_at"],
        updated_at=user["updated_at"],
        type=user["type"],
        image=user["image"],
    )


async def get_user_service(
    username: str,
    uow: MongoDBUnitOfWork[UserRepository] = Depends(
        uow_context_manager(UserRepository)
    ),
) -> UserOut:
    if (user := await uow.repo.get_by_name(username)) is None:
        raise exc.UserNotExist()
    return UserOut(
        username=user["username"],
        email=user["email"],
        _id=user["_id"],
        created_at=user["created_at"],
        updated_at=user["updated_at"],
        type=user["type"],
        image=user["image"],
    )


class UserData(BaseModel):
    username: str | None
    email: str | None
    password: str | None
    image: str | None

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


async def update_user_service(
    user_data: UserData,
    user: UserOut = Depends(get_current_user),
    uow: MongoDBUnitOfWork[UserRepository] = Depends(
        uow_context_manager(UserRepository)
    ),
) -> UserUpdateResponse:
    json_data: dict[str, dict[str, str | None]] = json.loads(user_data)
    if json_data["user_data"].get("image"):
        image = base64.b64decode((json_data["user_data"]["image"]))
        filename = get_user_image_filename(image)
        save_user_image(image, filename, user.username)

    upd_obj = UserUpdate(
        email=json_data["user_data"].get("email"),
        image=get_user_avatar_path(user.username) + "/" + filename
        if json_data["user_data"].get("image")
        else None,
        password=json_data["user_data"].get("password"),
    )
    updated_data = await uow.repo.update_user(user.id, upd_obj)
    return UserUpdateResponse(
        username=updated_data["username"],
        email=updated_data["email"],
        updated_at=updated_data["updated_at"],
        image=updated_data["image"],
    )
