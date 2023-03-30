import pytest
from src.db.schemas.user import UserIn
from src.repository.user import UserRepository
from tests.conftest import session_mock, mock_settings

USER = UserIn(
    username="test", email="test@mial.ru", password="test_hash_pass"
)


@pytest.fixture
async def repo(session_mock, mock_settings):
    return UserRepository(
        session_mock[0], session_mock[1], mock_settings.MONGODB_DATABASE
    )


@pytest.fixture
async def repo_with_user(repo):
    USER = UserIn(
        username="test", email="test@mial.ru", password="test_hash_pass"
    )
    id = await repo.add(USER.dict())
    await repo.session.commit_transaction()
    return repo, id


async def test_repository_can_get_by_name(repo_with_user):
    get_result = await repo_with_user[0].get_by_name(USER.username)
    assert get_result["username"] == USER.username


async def test_repository_can_get_by_id(repo_with_user):
    get_result = await repo_with_user[0].get_by_id(repo_with_user[1])
    assert get_result["username"] == USER.username


async def test_repository_can_count(repo_with_user):
    count = await repo_with_user[0].count({})
    assert count == 1