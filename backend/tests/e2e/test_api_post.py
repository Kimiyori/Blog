from datetime import datetime, timedelta
from jose import jwt
import pytest_asyncio
import pytest
from fastapi import status
from src.service.user import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    get_password_hash,
    SECRET_KEY,
    ALGORITHM,
)
from src.db.schemas.user import UserIn
from src.db.schemas.post import PostIn
from tests.conftest import session_mock, mock_settings, client_app


POST = PostIn(
    title="test", content=[{"data": {"type": "text", "text": "test"}, "order": 1}]
)


@pytest.fixture
async def user_data(session_mock):
    user = await session_mock[0].test.users.insert_one(
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
    return user.inserted_id, token


async def test_create_post(client_app, user_data):
    response = await client_app.post(
        "/post",
        data=POST.json(),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {user_data[1]}",
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    json = response.json()
    assert json["_id"]
    assert json["user_id"] == str(user_data[0])
    assert json["created_at"] == json["updated_at"]


async def test_create_post_not_auth(client_app):
    response = await client_app.post(
        "/post",
        data=POST.json(),
        headers={
            "Content-Type": "application/json",
        },
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_create_post_wrong_content_types(client_app, user_data):
    post = {
        "title": "test",
        "content": [{"data": {"type": "text", "image_url": "test"}, "order": 1}],
    }
    response = await client_app.post(
        "/post",
        data=post,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {user_data[1]}",
        },
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

