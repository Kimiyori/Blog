# pylint: disable=missing-class-docstring
from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Base settings for database"""

    MONGODB_ROOT_USER: str
    MONGODB_ROOT_PASSWORD: str
    MONGODB_PORT_NUMBER: int
    MONGODB_REPLICA_SET_NAME: str
    MONGODB_DATABASE: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

    @property
    def mongo_url(self) -> str:
        return (
            "mongodb://"
            f"{self.MONGODB_ROOT_USER}:{self.MONGODB_ROOT_PASSWORD}"
            f"@mongodb:{self.MONGODB_PORT_NUMBER}/"
            f"?replicaSet={self.MONGODB_REPLICA_SET_NAME}"
        )


@lru_cache()
def get_settings() -> Settings:
    return Settings()  # type:ignore
