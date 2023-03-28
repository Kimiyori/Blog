# pylint: disable=redefined-outer-name
import asyncio
import pytest
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseSettings


class SettingsMock(BaseSettings):
    MONGODB_ROOT_USER: str = "root"
    MONGODB_ROOT_PASSWORD: str = "rootpass"
    MONGODB_PORT_NUMBER: int = 27017
    MONGODB_REPLICA_SET_NAME: str = "replSet"
    MONGODB_DATABASE: str = "test"

    @property
    def mongo_url(self) -> str:
        return (
            "mongodb://"
            f"{self.MONGODB_ROOT_USER}:{self.MONGODB_ROOT_PASSWORD}"
            f"@mongodb:{self.MONGODB_PORT_NUMBER}/"
            f"?replicaSet={self.MONGODB_REPLICA_SET_NAME}"
        )


@pytest.fixture(scope="session", autouse=True)
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def mock_settings():
    settings = SettingsMock()
    settings.MONGODB_DATABASE = "test"
    return settings


@pytest.fixture(scope="session")
def client(mock_settings):
    return AsyncIOMotorClient(mock_settings.mongo_url)


@pytest.fixture
async def session_mock(client, mock_settings):
    try:
        async with await client.start_session() as session:
            async with session.start_transaction():
                yield client, session
    finally:
        await client.drop_database(mock_settings.MONGODB_DATABASE)