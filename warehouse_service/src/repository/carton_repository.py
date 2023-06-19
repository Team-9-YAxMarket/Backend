from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.db.db import get_session
from src.db.models import Carton
from src.repository.abstract_repository import AbstractRepository


class CartonRepository(AbstractRepository):
    """Репозиторий для работы с моделью Carton."""

    def __init__(self, session: AsyncSession = Depends(get_session)) -> None:
        super().__init__(session, Carton)

    async def get_carton(self, carton_type: str):
        """Возвращает информацию о доступных упаковках из базы данных."""
        statement = select(Carton).filter(Carton.carton_type == carton_type)
        carton_available = await self._session.execute(statement)
        return carton_available.scalar() or 0
