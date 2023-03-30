from bson import ObjectId
from fastapi import Depends
from src.db.schemas.post import PostIn, PostOut, PostCreate
from src.db.schemas.user import UserOut
from src.repository.post import PostRepository
from src.service.user import get_current_user
from src.unit_of_work import MongoDBUnitOfWork, uow_context_manager


async def create_post_service(
    post_data: PostIn,
    user: UserOut = Depends(get_current_user),
    uow: MongoDBUnitOfWork[PostRepository] = Depends(
        uow_context_manager(PostRepository)
    ),
) -> PostOut:
    dct_data = post_data.dict()
    dct_data["user_id"] = user.id
    post_id = await uow.repo.add(PostCreate(**dct_data).dict())
    post = await uow.repo.get_by_id(post_id)
    return PostOut(**post)


async def get_post_service(
    post_id: str,
    uow: MongoDBUnitOfWork[PostRepository] = Depends(
        uow_context_manager(PostRepository)
    ),
) -> PostOut:
    post = await uow.repo.get_by_id(ObjectId(post_id))
    return PostOut(**post)

async def delete_post_service(
    post_id: str,
    uow: MongoDBUnitOfWork[PostRepository] = Depends(
        uow_context_manager(PostRepository)
    ),
):
    await uow.repo.delete(ObjectId(post_id))
