from src.db.schemas.abc import PyObjectId
from src.repository.abc import MongoDbRepository
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorCollection,
    AsyncIOMotorClientSession,
)
from src.db.schemas.user import UserBase
from typing import TypedDict


class TypedReturn(TypedDict):
    _id: PyObjectId
    username: str
    password: str
    email: str | None


class UserRepository(MongoDbRepository[UserBase]):
    def __init__(
        self,
        client: AsyncIOMotorClient,
        session: AsyncIOMotorClientSession,
        database_name: str,
    ) -> None:
        super().__init__(client, session, database_name)
        self.collection: AsyncIOMotorCollection = self.database.users

    async def get_by_name(self, name: str) -> TypedReturn | None:
        user: TypedReturn | None = await self.collection.find_one(
            {"username": name}, session=self.session
        )
        return user
