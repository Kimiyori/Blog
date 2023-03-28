import pytest
from src.repository.abc import MongoDbRepository
from src.unit_of_work import MongoDBUnitOfWork
from tests.conftest import session_mock, mock_settings
from tests.integration.test_mongo import insert_users


@pytest.fixture
async def uow_factory(session_mock, mock_settings):
    uow = MongoDBUnitOfWork(session_mock, mock_settings)
    async with uow(MongoDbRepository) as uow_session:
        yield uow_session


async def test_uow(uow_factory, session_mock):
    await insert_users(session_mock)
    count = await uow_factory.client.test.users.count_documents(
        {}, session=uow_factory.session
    )
    assert 3 == count


async def test_uow_back_committed_work_by_default(session_mock, mock_settings):
    uow = MongoDBUnitOfWork(session_mock, mock_settings)
    async with uow(MongoDbRepository) as uow_session:
        await insert_users(session_mock)
        await uow_session.commit()
    count = await uow.client.test.users.count_documents({})
    assert 3 == count


async def test_uow_back_uncommitted_work_by_default(session_mock, mock_settings):
    uow = MongoDBUnitOfWork(session_mock, mock_settings)
    async with uow(MongoDbRepository) as uow_session:
        await insert_users(session_mock)

    count = await uow.client.test.users.count_documents({})
    assert 0 == count


async def test_uow_rolls_back_on_error(session_mock, mock_settings):
    class MyException(Exception):
        pass

    uow = MongoDBUnitOfWork(session_mock, mock_settings)
    with pytest.raises(MyException):
        async with uow(MongoDbRepository) as uow_session:
            await insert_users(session_mock)
            raise MyException()

    count = await uow.client.test.users.count_documents({})
    assert 0 == count
