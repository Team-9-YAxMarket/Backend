from typing import Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.repository.abstract_repository import AbstractRepository

from src.db.models import SKU

from src.db.db import get_session


class SKURepository(AbstractRepository):
    """Репозиторий для работы с моделью SKU."""

    def __init__(self, session: AsyncSession = Depends(get_session)) -> None:
        super().__init__(session, SKU)

    async def get_sku_count(self, sku: str):
        """Проверяет наличие SKU на складе."""

        statement = select(SKU.count).filter(SKU.sku == sku)
        sku_available = await self._session.execute(statement)

        return sku_available.scalars().first() or 0

    async def get_sku_info(self ,sku:str) ->Optional[SKU]:
        """Возвращает информацию о характеристиках SKU."""
        sku_info = await self._session.execute(
            select(SKU).filter(SKU.sku == sku)
        )
        return sku_info.scalar()
