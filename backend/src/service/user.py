from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from src.db.schemas.user import UserOut, UserIn
from src.unit_of_work import uow_context_manager, MongoDBUnitOfWork
from src.repository.user import UserRepository
from passlib.context import CryptContext

SECRET_KEY = "3898b1713cd001b4e6b41be328ab344b697baff8b100da072ae6c62fdedd6f45"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token", scheme_name="JWT")


def get_password_hash(password: str) -> str:
    hash_pass: str = pwd_context.hash(password)
    return hash_pass


def verify_password(plain_password: str, hashed_password: str) -> bool:
    verify: bool = pwd_context.verify(plain_password, hashed_password)
    return verify


def create_access_token(
    data: dict[str, str | datetime], expires_delta: timedelta | None = None
) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta if expires_delta else timedelta(minutes=15)
    )
    to_encode.update({"exp": expire})
    encoded_jwt: str = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


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
    user_data.password = get_password_hash(user_data.password)
    created_id = await uow.repo.add(user_data.dict())
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
    if (user := await uow.repo.get_by_name(username)) is None:
        raise credentials_exception
    return UserOut(username=user["username"], _id=user["_id"], email=user["email"])
