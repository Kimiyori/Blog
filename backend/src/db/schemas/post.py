from datetime import datetime
from typing import Literal, Annotated
from pydantic import BaseModel, Field

from src.db.schemas.abc import MongoBaseModel, PyObjectId


class ImageBlock(BaseModel):
    type: Literal["image"]
    image_url: str
    description: str | None


class TextBlock(BaseModel):
    type: Literal["text"]
    text: str


class VideoBlock(BaseModel):
    type: Literal["video"]
    video_url: str


ContentType = Annotated[
    TextBlock | ImageBlock | VideoBlock, Field(..., discriminator="type")
]


class ContentPost(BaseModel):
    data: ContentType
    order: int


class PostBase(BaseModel):
    user_id: PyObjectId


class PostIn(BaseModel):
    title: str
    content: list[ContentPost]


class PostCreate(PostBase, PostIn):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class PostOut(MongoBaseModel, PostBase):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
