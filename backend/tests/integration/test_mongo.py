from src.db.schemas.user import UserIn
from src.service.user import get_password_hash
from tests.conftest import session_mock, mock_settings
import pytest

USERS = [
    UserIn(username=user, email=f"{user}@mail.ru", password=get_password_hash(user))
    for user in ["test1", "test2", "test3"]
]


async def insert_users(session_mock):
    await session_mock[0].test.users.insert_many(
        [dict(user) for user in USERS], session=session_mock[1]
    )


@pytest.mark.asyncio
async def test_users_can_load_lines(session_mock):
    await insert_users(session_mock)
    count = await session_mock[0].test.users.count_documents(
        {}, session=session_mock[1]
    )
    assert count == len(USERS)


@pytest.mark.asyncio
async def test_users_can_not_save_lines(session_mock):
    await insert_users(session_mock)
    await session_mock[1].abort_transaction()
    count = await session_mock[0].test.users.count_documents(
        {}, session=session_mock[1]
    )
    assert count == 0


@pytest.mark.asyncio
async def test_users_can_save_lines(session_mock):
    await insert_users(session_mock)
    await session_mock[1].commit_transaction()
    await session_mock[1].end_session()
    count = await session_mock[0].test.users.count_documents({})
    assert count == len(USERS)
