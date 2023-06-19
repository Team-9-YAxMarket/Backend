from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.db import get_session
from src.db.models import SKU, Cargotype, sku_cargotype_table
from src.repository.abstract_repository import AbstractRepository


class SKUCargotypeRepository(AbstractRepository):
    """Репозиторий для работы с моделью SKU и Cargotype."""

    def __init__(self, session: AsyncSession = Depends(get_session)):
        super().__init__(session, SKU)

    async def get_cargotypes_for_sku(self, sku: str) -> list[Cargotype]:
        """Возвращает список cargotype для указанного SKU."""
        sku_cargotypes = await self._session.execute(
            select(Cargotype)
            .join(sku_cargotype_table)
            .where(sku_cargotype_table.c.sku == sku)
        )
        cargotypes = [
            cargotype.cargotype for cargotype in sku_cargotypes.scalars().all()
        ]
        return cargotypes
