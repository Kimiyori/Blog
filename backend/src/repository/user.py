from fastapi import Request
from src.repository.abc import MongoDbRepository
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorCollection,
    AsyncIOMotorClientSession,
)
from src.db.schemas.user import UserBase


class UserRepository(MongoDbRepository[UserBase]):
    def __init__(
        self,
        client: AsyncIOMotorClient,
        session: AsyncIOMotorClientSession,
        request: Request,
    ) -> None:
        super().__init__(client, session, request)
        self.collection: AsyncIOMotorCollection = self.database.users

    async def get_by_name(self, name: str) -> dict[str, str | int] | None:
        user: dict[str, str | int] | None = await self.collection.find_one(
            {"username": name}, session=self.session
        )
        return user
