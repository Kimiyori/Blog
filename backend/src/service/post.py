from bson import ObjectId
from fastapi import Depends, HTTPException, status
from src.db.schemas.post import PostIn, PostOut, PostCreate, PostUpdate
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
    post_create = PostCreate(**post_data.dict(), user_id=user.id)
    post_id = await uow.repo.add(post_create.dict())
    await uow.commit()
    if (post := await uow.repo.get_by_id(post_id)) is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong. Pleasy try Again",
        )
    return PostOut(**post)


async def get_post_service(
    post_id: str,
    uow: MongoDBUnitOfWork[PostRepository] = Depends(
        uow_context_manager(PostRepository)
    ),
) -> PostOut:
    if (post := await uow.repo.get_by_id(post_id)) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="post with given id doesnt exist",
        )
    return PostOut(**post)


async def delete_post_service(
    post_id: str,
    user: UserOut = Depends(get_current_user),
    uow: MongoDBUnitOfWork[PostRepository] = Depends(
        uow_context_manager(PostRepository)
    ),
) -> None:
    await uow.repo.delete(ObjectId(post_id))
    await uow.commit()


async def update_post_service(
    post_id: str,
    post: PostUpdate,
    user: UserOut = Depends(get_current_user),
    uow: MongoDBUnitOfWork[PostRepository] = Depends(
        uow_context_manager(PostRepository)
    ),
) -> None:
    await uow.repo.update_post(post_id, post)
    await uow.commit()
