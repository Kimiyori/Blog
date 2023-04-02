from __future__ import annotations
from datetime import datetime
from typing import Literal, Annotated
from pydantic import BaseModel, Field, validator, root_validator

from src.db.schemas.abc import MongoBaseModel, PyObjectId


class ImageBlock(BaseModel):
    type: Literal["image"]
    url: str
    description: str | None


class TextBlock(BaseModel):
    type: Literal["text"]
    text: str


class VideoBlock(BaseModel):
    type: Literal["video"]
    url: str


ContentType = Annotated[
    TextBlock | ImageBlock | VideoBlock,
    Field(..., discriminator="type"),
]


def check_content_unique_order(list_content: list[ContentPost]) -> list[ContentPost]:
    if len(list_content) != len(set(block.order for block in list_content)):
        raise ValueError("must be different unique update order values")
    return list_content


class ContentPost(BaseModel):
    data: ContentType
    order: int
    main_block: bool = False

    @validator("order")
    def check_unique_update(cls, v: int) -> int:
        if v < 0:
            raise ValueError("must be ppositive")
        return v


class PostBase(BaseModel):
    user_id: PyObjectId
    title: str


class PostIn(BaseModel):
    title: str
    content: list[ContentPost] = []
    _normalize_content = validator("content", allow_reuse=True)(
        check_content_unique_order
    )


class PostCreate(PostBase):
    content: list[ContentPost] = []
    views: int = 1
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    _normalize_content = validator("content", allow_reuse=True)(
        check_content_unique_order
    )


class PostOut(MongoBaseModel, PostBase):
    created_at: datetime
    updated_at: datetime


class PostUpdate(BaseModel):
    title: str | None
    update_content: list[ContentPost] | None = []
    delete_content: list[int] = []
    _normalize_content = validator("update_content", allow_reuse=True)(
        check_content_unique_order
    )

    @root_validator()
    def check_unique_order_values_from_lists(cls, values):  # type:ignore
        upd = [block.order for block in values.get("update_content")]
        dlt = values.get("delete_content")
        if set(upd) & set(dlt):
            raise ValueError(
                "order values from delete and update lists must be different"
            )
        return values

    @validator("delete_content")
    def check_unique_delete(cls, v: list[int]) -> list[int]:
        if len(v) != len(set(v)):
            raise ValueError("must be different unique delete order values")
        return v
