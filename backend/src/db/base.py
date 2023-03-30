from typing import AsyncGenerator
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorClientSession
from fastapi import Depends, Request
from src.config import get_settings, Settings


def client_mongodb_factory(
    settings: Settings = Depends(get_settings),
) -> AsyncIOMotorClient:
    return AsyncIOMotorClient(settings.mongo_url)


async def async_mongo_session(
    request: Request,
) -> AsyncGenerator[AsyncIOMotorClientSession, None]:
    async with await request.app.mongo_client.start_session() as session:
        async with session.start_transaction():
            yield request.app.mongo_client, session
