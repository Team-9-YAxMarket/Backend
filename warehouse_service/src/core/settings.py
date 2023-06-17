import os
from functools import cache

from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """Настройки проекта."""

    DEBUG: bool = False
    WAREHOUSE_ROOT_PATH: str = ""
    WAREHOUSE_APP_DB_NAME: str = os.getenv('WAREHOUSE_APP_DB_NAME')
    WAREHOUSE_APP_DB_USER: str = os.getenv('WAREHOUSE_APP_DB_USER')
    WAREHOUSE_APP_DB_PASSWORD: str = os.getenv('WAREHOUSE_APP_DB_PASSWORD')
    DB_HOST: str = os.getenv('DB_HOST')
    DB_PORT: int = os.getenv('DB_PORT')

    @property
    def database_url(self) -> str:
        """Получить ссылку для подключения к DB."""
        return (
            "postgresql+asyncpg://"
            f"{self.WAREHOUSE_APP_DB_USER}:{self.WAREHOUSE_APP_DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.WAREHOUSE_APP_DB_NAME}"
        )
    # @property
    # def warehouse_url(self) - >:
    #

    class Config:
        env_file = ".env"


@cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
