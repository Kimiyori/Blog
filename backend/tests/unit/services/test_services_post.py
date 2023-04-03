# from datetime import timedelta, datetime
# from bson import ObjectId
# from fastapi import HTTPException
# import pytest
# from typing import Any
# from src.service.user import (
#     create_access_token,
#     authenticate_user,
#     create_new_user,
#     get_password_hash,
#     get_current_user,
#     SECRET_KEY,
#     ALGORITHM,
# )
# from jose import jwt
# from src.db.schemas.user import UserIn
# from src.repository.abc import AbstractRepository, T
# from src.unit_of_work import AbstractUnitOfWork


# USER = UserIn(username="test", email="text", password="test")


# class FakeRepository(AbstractRepository[T]):
#     def __init__(self, session: Any) -> None:
#         self.session = []

#     async def add(self, entity: T) -> None:
#         self.session.append(entity)
#         return len(self.session) - 1

#     def get(self, reference):
#         try:
#             return next(b for b in self.session if b["username"] == reference)
#         except StopIteration:
#             return None

#     async def get_by_name(self, name):
#         if (user := self.get(name)) is not None:
#             return user

#     async def get_by_id(self, id):
#         return self.session[id]

#     async def count(self, entity):
#         return len(self.session)


# class FakeUnitOfWork(AbstractUnitOfWork):
#     def __init__(self):
#         self.repo = FakeRepository([])
#         self.committed = False

#     async def commit(self):
#         self.committed = True

#     async def rollback(self):
#         pass


# @pytest.fixture
# def uow():
#     return FakeUnitOfWork()
