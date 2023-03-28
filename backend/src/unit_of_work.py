import abc
from typing import Any, AsyncGenerator, Callable, Generic, TypeVar
from pymongo.errors import OperationFailure, ConnectionFailure
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorClientSession
from fastapi import Depends
from src.config import get_settings, Settings
from src.db.base import async_mongo_session

UowT = TypeVar("UowT")


class AbstractUnitOfWork(abc.ABC, Generic[UowT]):
    """Abstract class for Unit of Work"""

    def __init__(self, session: Any) -> None:
        self.session = session

    def __call__(self, repo: Callable[..., UowT]) -> "AbstractUnitOfWork[UowT]":
        self.repo = repo(self.session)
        return self

    async def __aenter__(self) -> "AbstractUnitOfWork[UowT]":
        return self

    async def __aexit__(self, *args: Any) -> None:
        pass

    @abc.abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError


class MongoDBUnitOfWork(AbstractUnitOfWork[UowT]):
    """MongoDB instance unit of work"""

    def __init__(
        self,
        client: tuple[AsyncIOMotorClient, AsyncIOMotorClientSession] = Depends(
            async_mongo_session
        ),
        settings: Settings = Depends(get_settings),
    ) -> None:
        super().__init__(client[1])
        self.client = client[0]
        self.settings = settings

    def __call__(self, repo: Callable[..., UowT]) -> AbstractUnitOfWork[UowT]:
        self.repo = repo(self.client, self.session, self.settings.MONGODB_DATABASE)
        return self

    async def commit(self) -> None:
        while True:
            try:
                # Commit uses write concern set at transaction start.
                await self.session.commit_transaction()
                print("Transaction committed.")
                break
            except (ConnectionFailure, OperationFailure) as exc:
                # Can retry commit
                if exc.has_error_label("UnknownTransactionCommitResult"):
                    print(
                        "UnknownTransactionCommitResult, retrying commit operation ..."
                    )
                    continue
                print("Error during commit ...")
                raise

    async def rollback(self) -> None:
        await self.session.abort_transaction()


def uow_context_manager(
    repo: Callable[..., UowT],
) -> Callable[
    [AbstractUnitOfWork[UowT]], AsyncGenerator[AbstractUnitOfWork[UowT], None]
]:
    async def wrapper(
        uow: AbstractUnitOfWork[UowT] = Depends(MongoDBUnitOfWork),
    ) -> AsyncGenerator[AbstractUnitOfWork[UowT], None]:
        async with uow(repo) as session:
            yield session

    return wrapper
