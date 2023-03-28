from datetime import datetime, timedelta
import pytest_asyncio
import pytest
from fastapi import status
from src.db.base import async_mongo_session
from src.service.user import ALGORITHM, SECRET_KEY
from src.service.user import ACCESS_TOKEN_EXPIRE_MINUTES
from src.service.user import get_password_hash
from httpx import AsyncClient
from src.db.schemas.user import UserWithPassword
from src.main import create_app
from tests.conftest import session_mock, mock_settings
from src.config import get_settings
from jose import jwt, JWTError


@pytest_asyncio.fixture()
async def session_wrapper(session_mock):
    async def wrapper():
        return session_mock

    return wrapper

@pytest_asyncio.fixture()
async def settings_wrapper(mock_settings):
    async def wrapper():
        return mock_settings

    return wrapper

@pytest.fixture
@pytest.mark.anyio
async def client(session_wrapper,settings_wrapper) -> AsyncClient:
    app = create_app()
    app.dependency_overrides[get_settings] = settings_wrapper
    app.dependency_overrides[async_mongo_session] = session_wrapper
    async with AsyncClient(app=app, base_url="http://test") as c:
        yield c



async def test_create_user(client):
    user_data = UserWithPassword(username="test", email="test", password="test")
    response = await client.post(
        "/users", data=user_data.json(), headers={"Content-Type": "application/json"}
    )
    assert response.status_code == status.HTTP_201_CREATED
    for x in ["access_token", "token_type"]:
        assert x in response.json().keys()


async def test_create_user_already_exist(client, session_mock):
    user_data = UserWithPassword(username="test", email="test", password="test")
    await session_mock[0].test.users.insert_one(
        dict(user_data),
        session=session_mock[1],
    )
    response = await client.post(
        "/users", data=user_data.json(), headers={"Content-Type": "application/json"}
    )
    assert response.status_code == status.HTTP_409_CONFLICT


async def test_get_token(client, session_mock):
    await session_mock[0].test.users.insert_one(
        {
            "username": "test",
            "email": "test@mial.ru",
            "password": get_password_hash("test"),
        },
        session=session_mock[1],
    )
    response = await client.post(
        "/users/token",
        data={"username": "test", "password": "test"},
        headers={"content-type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["access_token"] is not None
    assert response.json()["token_type"] == "bearer"


async def test_get_token_user_not_exist(client):
    response = await client.post(
        "/users/token",
        data={"username": "test", "password": "test"},
        headers={"content-type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Incorrect username or password"}


async def test_get_token_wrong_password(client, session_mock):
    await session_mock[0].test.users.insert_one(
        {
            "username": "test",
            "email": "test@mial.ru",
            "password": get_password_hash("test"),
        },
        session=session_mock[1],
    )
    response = await client.post(
        "/users/token",
        data={"username": "test", "password": "wrong_test"},
        headers={"content-type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Incorrect username or password"}


async def test_get_me(client, session_mock):
    await session_mock[0].test.users.insert_one(
        {
            "username": "test",
            "email": "test@mial.ru",
            "password": get_password_hash("test"),
        },
        session=session_mock[1],
    )
    token = jwt.encode(
        {
            "sub": "test",
            "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        },
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
    response = await client.get(
        "/users/me",
        headers={
            "content-type": "application/x-www-form-urlencoded",
            "Authorization": f"Bearer {token}",
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"email": "test@mial.ru", "username": "test"}


async def test_get_me_not_username(client, session_mock):
    await session_mock[0].test.users.insert_one(
        {
            "username": "test",
            "email": "test@mial.ru",
            "password": get_password_hash("test"),
        },
        session=session_mock[1],
    )
    token = jwt.encode(
        {
            "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        },
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
    response = await client.get(
        "/users/me",
        headers={
            "content-type": "application/x-www-form-urlencoded",
            "Authorization": f"Bearer {token}",
        },
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Could not validate credentials"}


async def test_get_me_jwt_error(client, session_mock):
    await session_mock[0].test.users.insert_one(
        {
            "username": "test",
            "email": "test@mial.ru",
            "password": get_password_hash("test"),
        },
        session=session_mock[1],
    )
    response = await client.get(
        "/users/me",
        headers={
            "content-type": "application/x-www-form-urlencoded",
            "Authorization": f"Bearer error_token",
        },
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Could not validate credentials"}


async def test_get_me_user_not_exist(client):
    token = jwt.encode(
        {
            "sub": "test",
            "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        },
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
    response = await client.get(
        "/users/me",
        headers={
            "content-type": "application/x-www-form-urlencoded",
            "Authorization": f"Bearer {token}",
        },
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Could not validate credentials"}