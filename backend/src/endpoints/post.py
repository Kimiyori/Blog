from fastapi import APIRouter, Depends, status, Response
from src.service.post import create_post_service, get_post_service, delete_post_service
from src.db.schemas.post import PostIn, PostOut

router = APIRouter(
    prefix="/post",
    tags=["post"],
)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_post(post: PostIn = Depends(create_post_service)) -> PostOut:
    return post


@router.get("/{post_id}", status_code=status.HTTP_200_OK)
async def get_post(post: PostIn = Depends(get_post_service)) -> PostOut:
    return post


@router.delete(
    "/{post_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None
)
async def delete_post(post: PostIn = Depends(delete_post_service)) -> Response:
    return Response()
