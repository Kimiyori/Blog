from pydantic import BaseModel


# class PyObjectId(ObjectId):
#     @classmethod
#     def __get_validators__(cls):
#         yield cls.validate

#     @classmethod
#     def validate(cls, v):
#         if not ObjectId.is_valid(v):
#             raise ValueError("Invalid objectid")
#         return ObjectId(v)

#     @classmethod
#     def __modify_schema__(cls, field_schema):
#         field_schema.update(type="string")


# class MongoBaseModel(BaseModel):
#     id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

#     class Config:
#         json_encoders = {ObjectId: str}
#         orm_mode = True


class UserBase(BaseModel):
    username: str
    email: str | None = None

    class Config:
        orm_mode = True


class UserWithPassword(UserBase):
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
