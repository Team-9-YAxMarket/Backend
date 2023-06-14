from typing import Any

from sqlalchemy import select

from src.repository.abstract_repository import AbstractRepository

from src.db.models import SKU


class SKURepository(AbstractRepository):
    """Репозиторий для работы с моделью SKU."""
    async def get_cargotypes(self, req_sku: str, req_count: int):
        """Возвращает все объекты модели из базы данных."""

        statement = select(SKU).filter(SKU.sku == req_sku, SKU.in_stock >= req_count)
        sku = await self._session.execute(statement)
        if not sku:
            return []

        cargotypes = await self._sku_cargo_repository.get_cargotypes_for_sku(SKU.sku)

        # Дальнейшая обработка и возврат данных

        return cargotypes

