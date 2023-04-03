from pydantic import BaseModel
from src.db.schemas.abc import MongoBaseModel


class UserBase(BaseModel):
    username: str
    email: str | None = None


class UserIn(UserBase):
    password: str


class UserOut(MongoBaseModel, UserBase):
    ...


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
