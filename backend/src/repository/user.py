from bson import ObjectId
from pymongo import ReturnDocument
from src.db.schemas.abc import PyObjectId
from src.repository.abc import MongoDbRepository
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorCollection,
    AsyncIOMotorClientSession,
)
from src.db.schemas.user import UserBase, UserUpdate
from typing import TypedDict


class TypedReturn(TypedDict):
    _id: PyObjectId
    username: str
    password: str
    email: str | None
    image: str | None


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

    async def update_user(
        self, user_id: PyObjectId, updated_data: UserUpdate
    ) -> TypedReturn | None:
        updated_user: TypedReturn | None = await self.collection.find_one_and_update(
            {"_id": ObjectId(user_id)},
            {"$set": updated_data.dict(exclude_none=True)},
            projection={
                "password": False,
            },
            session=self.session,
            return_document=ReturnDocument.AFTER,
        )
        return updated_user
