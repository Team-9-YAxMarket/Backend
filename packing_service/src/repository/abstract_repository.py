import abc
from typing import TypeVar

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core import exceptions

DatabaseModel = TypeVar("DatabaseModel")


class AbstractRepository(abc.ABC):
    """Abstract class for Repository pattern implementation."""

    def __init__(self, session: AsyncSession, model: DatabaseModel) -> None:
        self._session = session
        self._model = model

    async def create(self, instance: DatabaseModel) -> DatabaseModel:
        self._session.add(instance)
        try:
            await self._session.commit()
        except IntegrityError:
            await self._session.rollback()
            raise exceptions.ObjectAlreadyExistsError(instance)

        return instance

    async def get_all(self) -> list[DatabaseModel]:
        """Возвращает все объекты модели из базы данных."""
        objects = await self._session.execute(select(self._model))
        return objects.scalars().all()
