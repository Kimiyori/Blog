from datetime import datetime
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from src.utils.auth import (
    get_password_hash,
    require_refresh_token,
    create_access_token,
    verify_password,
    oauth2_scheme,
    SECRET_KEY,
    REFRESH_SECRET_KEY,
    ALGORITHM,
)
from src.db.schemas.user import UserOut, UserIn, UserCreate
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
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="user or email already exist"
        )
    user_create = UserCreate(
        username=user_data.username,
        password=get_password_hash(user_data.password),
        email=user_data.email,
    )
    created_id = await uow.repo.add(user_create.dict())
    await uow.commit()
    new_user = await uow.repo.get_by_id(created_id)
    assert new_user
    return UserOut(**new_user)


async def authenticate_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    uow: MongoDBUnitOfWork[UserRepository] = Depends(
        uow_context_manager(UserRepository)
    ),
) -> UserIn | bool:
    if (user := await uow.repo.get_by_name(form_data.username)) is None:
        return False
    if not verify_password(form_data.password, user["password"]):
        return False
    return UserIn(
        username=user["username"], password=user["password"], email=user["email"]
    )


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    uow: MongoDBUnitOfWork[UserRepository] = Depends(
        uow_context_manager(UserRepository)
    ),
) -> UserOut:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if (username := payload.get("sub")) is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    if datetime.fromtimestamp(payload.get("exp")) < datetime.now():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if (user := await uow.repo.get_by_name(username)) is None:
        raise credentials_exception
    return UserOut(username=user["username"], _id=user["_id"], email=user["email"])


async def refresh_token_service(
    token: str = Depends(require_refresh_token),
    uow: MongoDBUnitOfWork[UserRepository] = Depends(
        uow_context_manager(UserRepository)
    ),
) -> str:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        if (username := payload.get("sub")) is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    if datetime.fromtimestamp(payload.get("exp")) < datetime.now():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if (user := await uow.repo.get_by_name(username)) is None:
        raise credentials_exception
    access_token: str = create_access_token(
        data={"sub": user["username"]},
    )
    return access_token
