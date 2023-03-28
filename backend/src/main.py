from fastapi import FastAPI
from src.endpoints import user


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(user.router)
    return app
