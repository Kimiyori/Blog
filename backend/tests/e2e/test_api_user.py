from datetime import datetime, timedelta
from unittest import mock
import pytest_asyncio
import pytest
from fastapi import status
from src.utils.auth import (
    ALGORITHM,
    SECRET_KEY,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    get_password_hash,
    create_refresh_token,
)
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
    for x in ["access_token"]:
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
    assert response.cookies.get("access_token") is not None
    assert response.cookies.get("refresh_token") is not None


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
        },
        cookies={"access_token": f"Bearer {token}"},
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
        },
        cookies={"access_token": f"Bearer {token}"},
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
        },
        cookies={"access_token": f"Bearer error"},
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
        },
        cookies={"access_token": f"Bearer {token}"},
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Could not validate credentials"}


async def test_refresh_token(client_app, session_mock):
    await session_mock[0].test.users.insert_one(
        {
            "username": "test",
            "email": "test@mial.ru",
            "password": get_password_hash("test"),
        },
        session=session_mock[1],
    )
    token = create_refresh_token(data={"sub": "test"})

    response = await client_app.get(
        "/users/refresh",
        cookies={"refresh_token": f"Bearer {token}"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["access_token"]
    assert response.cookies.get("access_token")


async def test_refresh_token_not_send_token(client_app, session_mock):
    await session_mock[0].test.users.insert_one(
        {
            "username": "test",
            "email": "test@mial.ru",
            "password": get_password_hash("test"),
        },
        session=session_mock[1],
    )

    response = await client_app.get(
        "/users/refresh",
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_get_user_by_name(client_app, session_mock):
    await session_mock[0].test.users.insert_one(
        {
            "username": "test",
            "email": "test@mial.ru",
            "password": get_password_hash("test"),
        },
        session=session_mock[1],
    )
    response = await client_app.get(
        "/users/test",
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == 'test'

async def test_get_user_by_name_not_found(client_app):

    response = await client_app.get(
        "/users/wrong",
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND