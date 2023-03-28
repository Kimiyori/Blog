from bson import ObjectId
from src.repository.abc import MongoDbRepository
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorCollection,
    AsyncIOMotorClientSession,
)
from src.db.schemas.user import UserBase, UserWithPassword


class UserRepository(MongoDbRepository[UserBase]):
    def __init__(
        self,
        client: AsyncIOMotorClient,
        session: AsyncIOMotorClientSession,
        database_name: str,
    ) -> None:
        super().__init__(client, session, database_name)
        self.collection: AsyncIOMotorCollection = self.database.users

    async def get_by_name(self, name: str) -> UserWithPassword | None:
        if (
            user := await self.collection.find_one(
                {"username": name}, session=self.session
            )
        ) is not None:
            return UserWithPassword(**user)
        return None

    async def get_by_id(self, id: ObjectId) -> UserBase | None:
        if (
            user := await self.collection.find_one({"_id": id}, session=self.session)
        ) is not None:
            return UserWithPassword(**user)
        return None
