from functools import cache
from pathlib import Path
from typing import List

from pydantic import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    """Настройки проекта."""

    DEBUG: bool = False
    ROOT_PATH: str = ""
    PACKING_ROOT_PATH: str = ROOT_PATH + "packing-service/"
    PACKING_APP_DB_NAME: str
    PACKING_APP_DB_USER: str
    PACKING_APP_DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    CORS_ORIGINS: List[str] = ["*"]

    @property
    def database_url(self) -> str:
        """Получить ссылку для подключения к DB."""
        return (
            "postgresql+asyncpg://"
            f"{self.PACKING_APP_DB_USER}:{self.PACKING_APP_DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.PACKING_APP_DB_NAME}"
        )

    class Config:
        env_file = ".env"


@cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
