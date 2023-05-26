# pylint: disable=redefined-outer-name
import asyncio
from contextlib import asynccontextmanager
import time
from unittest import mock
import pytest
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseSettings
import pytest_asyncio
from src.main import create_app
from src.db.base import async_mongo_session
from httpx import AsyncClient
from asgi_lifespan import LifespanManager


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
    time.sleep(1)
    try:
        async with await client.start_session() as session:
            async with session.start_transaction():
                yield client, session
    finally:
        await client.drop_database(mock_settings.MONGODB_DATABASE)


@pytest.fixture
async def session_wrapper(session_mock):
    async def wrapper():
        return session_mock

    return wrapper


@pytest_asyncio.fixture(scope="session")
async def lifespan(mock_settings, client):
    @asynccontextmanager
    async def wrapper(app):
        app.mongo_settings = mock_settings
        app.mongo_client = client
        yield

    return wrapper


@pytest.fixture
async def client_app(session_wrapper, lifespan) -> AsyncClient:
    time.sleep(1)
    app = create_app(lifespan)
    app.dependency_overrides[async_mongo_session] = session_wrapper
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://test") as c:
            yield c


@pytest.fixture
def mock_request(mock_settings):
    m = mock.Mock()
    m.app.mongo_settings = mock_settings
    return m
