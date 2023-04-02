from datetime import datetime, timedelta
from unittest import mock
import pytest_asyncio
import pytest
from fastapi import status
from src.service.user import ALGORITHM, SECRET_KEY
from src.service.user import ACCESS_TOKEN_EXPIRE_MINUTES
from src.service.user import get_password_hash
from src.db.schemas.user import UserIn
from tests.conftest import session_mock, mock_settings, client_app, lifespan
from jose import jwt


async def test_create_user_already_exist(client_app, session_mock):
    user_data = UserIn(username="test", email="test", password="test")
    await session_mock[0].test.users.insert_one(
        dict(user_data),
        session=session_mock[1],
    )
    response = await client_app.post(
        "/users", data=user_data.json(), headers={"Content-Type": "application/json"}
    )
    assert response.status_code == status.HTTP_409_CONFLICT


async def test_create_user(client_app):
    user_data = UserIn(username="test", email="test", password="test")
    response = await client_app.post(
        "/users", data=user_data.json(), headers={"Content-Type": "application/json"}
    )
    assert response.status_code == status.HTTP_201_CREATED
    for x in ["access_token", "token_type"]:
        assert x in response.json().keys()


async def test_get_token(client_app, session_mock):
    await session_mock[0].test.users.insert_one(
        {
            "username": "test",
            "email": "test@mial.ru",
            "password": get_password_hash("test"),
        },
        session=session_mock[1],
    )
    response = await client_app.post(
        "/users/token",
        data={"username": "test", "password": "test"},
        headers={"content-type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["access_token"] is not None
    assert response.json()["token_type"] == "bearer"


async def test_get_token_user_not_exist(client_app):
    response = await client_app.post(
        "/users/token",
        data={"username": "test", "password": "test"},
        headers={"content-type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Incorrect username or password"}


async def test_get_token_wrong_password(client_app, session_mock):
    await session_mock[0].test.users.insert_one(
        {
            "username": "test",
            "email": "test@mial.ru",
            "password": get_password_hash("test"),
        },
        session=session_mock[1],
    )
    response = await client_app.post(
        "/users/token",
        data={"username": "test", "password": "wrong_test"},
        headers={"content-type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Incorrect username or password"}


async def test_get_me(client_app, session_mock):
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
    response = await client_app.get(
        "/users/me",
        headers={
            "content-type": "application/x-www-form-urlencoded",
            "Authorization": f"Bearer {token}",
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == "test"
    assert response.json()["email"] == "test@mial.ru"


async def test_get_me_not_username(client_app, session_mock):
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
    response = await client_app.get(
        "/users/me",
        headers={
            "content-type": "application/x-www-form-urlencoded",
            "Authorization": f"Bearer {token}",
        },
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Could not validate credentials"}


async def test_get_me_jwt_error(client_app, session_mock):
    await session_mock[0].test.users.insert_one(
        {
            "username": "test",
            "email": "test@mial.ru",
            "password": get_password_hash("test"),
        },
        session=session_mock[1],
    )
    response = await client_app.get(
        "/users/me",
        headers={
            "content-type": "application/x-www-form-urlencoded",
            "Authorization": f"Bearer error_token",
        },
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Could not validate credentials"}


async def test_get_me_user_not_exist(client_app):
    token = jwt.encode(
        {
            "sub": "test",
            "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        },
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
    response = await client_app.get(
        "/users/me",
        headers={
            "content-type": "application/x-www-form-urlencoded",
            "Authorization": f"Bearer {token}",
        },
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Could not validate credentials"}
