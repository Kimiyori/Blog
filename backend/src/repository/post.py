from bson import ObjectId
from src.db.schemas.post import PostUpdate
from src.repository.abc import MongoDbRepository
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorCollection,
    AsyncIOMotorClientSession,
)
from pymongo import UpdateOne
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

    async def update_post(self, post_id: str, data: PostUpdate) -> None:
        query = [
            {
                "$set": data.dict(
                    exclude={"update_content", "delete_content"}, exclude_none=True
                )
            },
        ]
        query.extend(
            [
                {
                    "$set": {
                        "content": {
                            "$cond": [
                                {"$in": [block.order, "$content.order"]},
                                {
                                    "$map": {
                                        "input": "$content",
                                        "in": {
                                            "$mergeObjects": [
                                                "$$this",
                                                {
                                                    "$cond": [
                                                        {
                                                            "$eq": [
                                                                "$$this.order",
                                                                block.order,
                                                            ]
                                                        },
                                                        block.dict(),
                                                        {},
                                                    ]
                                                },
                                            ]
                                        },
                                    }
                                },
                                {"$concatArrays": ["$content", [block.dict()]]},
                            ]
                        },
                    }
                }
                for block in data.update_content
            ]
        )
        query.extend(
            [
                {
                    "$project": {
                        "title": 1,
                        "content": {
                            "$filter": {
                                "input": "$content",
                                "cond": {"$ne": ["$$this.order", order]},
                            }
                        },
                    }
                }
                for order in data.delete_content
            ]
        )
        result = await self.collection.update_one(
            {"_id": ObjectId(post_id)},
            query,
            session=self.session,
        )
