from datetime import timedelta, datetime
from bson import ObjectId
from fastapi import HTTPException
import pytest
from typing import Any
from src.service.user import (
    create_new_user,
    get_current_user,
)
from src.service.auth import authenticate_user
from src.utils.auth import ALGORITHM,SECRET_KEY,get_password_hash
from src.utils.auth import create_access_token
from jose import jwt
from src.db.schemas.user import UserIn
from src.repository.abc import AbstractRepository, T
from src.unit_of_work import AbstractUnitOfWork


USER = UserIn(username="test", email="text", password=get_password_hash("test"))


class FakeRepository(AbstractRepository[T]):
    def __init__(self, session: Any) -> None:
        self.session = []

    async def add(self, entity: T) -> None:
        self.session.append(entity)
        return len(self.session) - 1

    def get(self, reference):
        try:
            return next(b for b in self.session if b["username"] == reference)
        except StopIteration:
            return None

    async def get_by_name(self, name):
        if (user := self.get(name)) is not None:
            return user

    async def get_by_id(self, id):
        return self.session[id]

    async def count(self, entity):
        return len(self.session)


class FakeUnitOfWork(AbstractUnitOfWork):
    def __init__(self):
        self.repo = FakeRepository([])
        self.committed = False

    async def commit(self):
        self.committed = True

    async def rollback(self):
        pass

    async def refresh(self, entity):
        pass


@pytest.fixture
def uow():
    return FakeUnitOfWork()


def test_create_access_token():
    token = create_access_token(
        data={"sub": USER.username}, expires_delta=timedelta(minutes=30)
    )
    assert isinstance(token, str)


@pytest.mark.asyncio
async def test_create_user(uow):
    await create_new_user(USER, uow)
    assert uow.repo.get(USER.username) is not None
    assert uow.repo.get(USER.username)["username"] == USER.username
    assert uow.committed == True


@pytest.mark.asyncio
async def test_create_user_already_exist(uow):
    await uow.repo.add(dict(USER))
    with pytest.raises(HTTPException) as error:
        await create_new_user(USER, uow)
    assert error.value.detail == "user or email already exist"


@pytest.mark.asyncio
async def test_auth_user_not_exist_user(uow):
    auth = await authenticate_user(USER, uow)
    assert auth == False


@pytest.mark.asyncio
async def test_auth_user_wrong_pass(uow):
    await uow.repo.add(dict(USER))
    USER.password = "wrong_pass"
    auth = await authenticate_user(USER, uow)
    assert auth == False


@pytest.mark.asyncio
async def test_auth_user(uow):
    await uow.repo.add(
        {
            "username": USER.username,
            "email": USER.email,
            "password": get_password_hash(USER.password),
        }
    )
    auth = await authenticate_user(USER, uow)
    assert auth.username == USER.username


@pytest.mark.asyncio
async def test_get_current_user(uow):
    await uow.repo.add(
        {
            "_id": ObjectId(),
            "username": USER.username,
            "email": USER.email,
            "password": get_password_hash(USER.password),
        }
    )
    token = jwt.encode(
        {"sub": USER.username, "exp": datetime.utcnow() + timedelta(minutes=30)},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
    cur_user = await get_current_user(token, uow)
    assert cur_user.username == USER.username


@pytest.mark.asyncio
async def test_get_current_user_wrong_token_scheme(uow):
    await uow.repo.add(
        {
            "username": USER.username,
            "email": USER.email,
            "password": get_password_hash(USER.password),
        }
    )
    token = jwt.encode(
        {"exp": datetime.utcnow() + timedelta(minutes=30)},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
    with pytest.raises(HTTPException):
        await get_current_user(token, uow)


@pytest.mark.asyncio
async def test_get_current_user_user_no_exist(uow):
    token = jwt.encode(
        {"sub": USER.username, "exp": datetime.utcnow() + timedelta(minutes=30)},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
    with pytest.raises(HTTPException):
        await get_current_user(token, uow)
