from typing import AsyncIterator
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from src.config import get_settings
from src.endpoints import user, post, auth


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    app.mongo_settings = get_settings()  # type:ignore
    app.mongo_client = AsyncIOMotorClient(app.mongo_settings.mongo_url)  # type:ignore
    yield
    app.mongo_client.close()  # type:ignore


def create_app(lifespan_func=lifespan) -> FastAPI:  # type:ignore
    app = FastAPI(lifespan=lifespan_func)
    app.include_router(user.router)
    app.include_router(post.router)
    app.include_router(auth.router)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app