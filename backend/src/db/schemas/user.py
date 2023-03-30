from pydantic import BaseModel
from src.db.schemas.abc import MongoBaseModel


class UserBase(BaseModel):
    username: str
    email: str | None = None

    class Config:
        orm_mode = True


class UserIn(UserBase):
    password: str


class UserOut(UserBase, MongoBaseModel):
    ...


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
