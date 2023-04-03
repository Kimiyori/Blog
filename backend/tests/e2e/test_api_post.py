from datetime import datetime, timedelta
from bson import ObjectId
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
from src.db.schemas.post import PostIn, PostUpdate
from tests.conftest import session_mock, mock_settings, client_app, client


POST = PostIn(
    title="test",
    content=[
        {"data": {"type": "text", "text": "test"}, "order": 1},
        {"data": {"type": "text", "text": "test2"}, "order": 2},
    ],
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


async def test_get_post(client_app, session_mock, user_data):
    post = POST.dict()
    post["user_id"] = user_data[0]
    post["created_at"] = post["updated_at"] = datetime.now()
    post['views'] = 1
    post = await session_mock[0].test.posts.insert_one(
        post,
        session=session_mock[1],
    )
    response = await client_app.get(
        f"/post/{str(post.inserted_id)}",
        headers={
            "Content-Type": "application/json",
        },
    )
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert json["_id"]
    assert json["user_id"] == str(user_data[0])
    assert json["created_at"] and json["updated_at"]
    assert json['views'] == 2
    response2 = await client_app.get(
        f"/post/{str(post.inserted_id)}",
        headers={
            "Content-Type": "application/json",
        },
    )
    assert response2.status_code == status.HTTP_200_OK
    json = response2.json()
    assert json['views'] == 3


async def test_get_post_not_exist(client_app):
    response = await client_app.get(f"/post/{ObjectId()}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_delete_post(client_app, session_mock, user_data):
    post = POST.dict()
    post["user_id"] = user_data[0]
    post = await session_mock[0].test.posts.insert_one(
        post,
        session=session_mock[1],
    )
    response = await client_app.delete(
        f"/post/{str(post.inserted_id)}",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {user_data[1]}",
        },
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


async def test_delete_post_not_exist(client_app, user_data):
    response = await client_app.delete(
        f"/post/{ObjectId()}",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {user_data[1]}",
        },
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


async def test_update_post(client_app, session_mock, user_data, client):
    post = POST.dict()
    post["user_id"] = user_data[0]
    post_id = await session_mock[0].test.posts.insert_one(
        post,
        session=session_mock[1],
    )
    updated_post = PostUpdate(
        title="updated_post",
        update_content=[
            {"data": {"type": "image", "url": "image"}, "order": 3},
            {"data": {"type": "text", "text": "new_text"}, "order": 1},
        ],
        delete_content=[2],
    )
    response = await client_app.put(
        f"/post/{str(post_id.inserted_id)}",
        data=updated_post.json(),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {user_data[1]}",
        },
    )
    assert response.status_code == status.HTTP_200_OK
    async with await client.start_session() as session:
        async with session.start_transaction():
            expected = await client.test.posts.aggregate(
                [
                    {"$match": {"_id": post_id.inserted_id}},
                    {"$sort": {"content.order": 1}},
                ],
                session=session,
            ).to_list(1)
            expected = expected[0]
            assert expected["title"] == updated_post.title
            assert len(expected["content"]) == 2
            assert expected["content"][0]["data"]["text"] == "new_text"
            assert expected["content"][1] == updated_post.update_content[0].dict()

async def test_update_post_not_auth(client_app, session_mock):
    post = POST.dict()
    post_id = await session_mock[0].test.posts.insert_one(
        post,
        session=session_mock[1],
    )
    updated_post = PostUpdate(
        title="updated_post",
        update_content=[
            {"data": {"type": "image", "url": "image"}, "order": 3},
            {"data": {"type": "text", "text": "new_text"}, "order": 1},
        ],
        delete_content=[2],
    )
    response = await client_app.put(
        f"/post/{str(post_id.inserted_id)}",
        data=updated_post.json(),
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    