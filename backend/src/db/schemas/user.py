from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field
from src.db.schemas.abc import MongoBaseModel


class UserBase(BaseModel):
    username: str
    email: str | None = None


class UserType(str, Enum):
    user = "user"
    admin = "admin"


class UserIn(UserBase):
    password: str


class UserCreate(UserBase):
    password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    type: UserType = UserType.user
    image: str | None = None


class UserOut(MongoBaseModel, UserBase):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    type: UserType = UserType.user
    image: str | None


class Token(BaseModel):
    access_token: str


class TokenData(BaseModel):
    username: str | None = None


class UserUpdate(MongoBaseModel, BaseModel):
    email: str | None
    image: str | None
    password: str | None
    updated_at: datetime = datetime.now()


class UserUpdateResponse(MongoBaseModel, BaseModel):
    username: str
    email: str | None
    image: str | None
    updated_at: datetime = datetime.now()
