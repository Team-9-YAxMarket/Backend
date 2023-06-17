from typing import Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.db import get_session
from src.db.models import Carton
from src.repository.abstract_repository import AbstractRepository


class CartonRepository(AbstractRepository):
    """Репозиторий для работы с моделью Carton."""

    def __init__(self, session: AsyncSession = Depends(get_session)) -> None:
        super().__init__(session, Carton)

    async def get_carton_by_carton_type(
        self, carton_type: str
    ) -> Optional[Carton]:
        carton = await self._session.execute(
            select(Carton).where(Carton.carton_type == carton_type)
        )
        return carton.scalars().first()
