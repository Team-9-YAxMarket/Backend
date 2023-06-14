from typing import Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.db import get_session
from src.db.models import SKU
from src.repository.abstract_repository import AbstractRepository


class SKURepository(AbstractRepository):
    """Репозиторий для работы с моделью SKU."""

    def __init__(self, session: AsyncSession = Depends(get_session)) -> None:
        super().__init__(session, SKU)

    async def get_sku_by_name_or_none(self, sku: str) -> Optional[SKU]:
        sku = await self._session.execute(select(SKU).where(SKU.sku == sku))
        return sku.scalars().first()
