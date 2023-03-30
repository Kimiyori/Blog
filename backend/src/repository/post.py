from src.repository.abc import MongoDbRepository
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorCollection,
    AsyncIOMotorClientSession,
)
from src.db.schemas.post import PostBase


class PostRepository(MongoDbRepository[PostBase]):
    def __init__(
        self,
        client: AsyncIOMotorClient,
        session: AsyncIOMotorClientSession,
        database_name: str,
    ) -> None:
        super().__init__(client, session, database_name)
        self.collection: AsyncIOMotorCollection = self.database.posts

    