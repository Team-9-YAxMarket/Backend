from typing import Any

from fastapi import Depends
from src.repository.sku_cargo_repository import SKUCargotypeRepository
from src.repository.sku_repository import SKURepository


class SKUService:
    def __init__(
            self,
            sku_repository: SKURepository = Depends(),
            sku_cargotype_repository: SKUCargotypeRepository = Depends(),
    ) -> None:
        self.__sku_repository = sku_repository
        self.__sku_cargotype_repository = sku_cargotype_repository
    """Сервис для работы с SKU."""

    async def cargotypes(self, sku: str, count: int):
        """Возвращает список SKU с информацией о cargotype."""
        return await self.__sku_repository.get_cargotypes(sku, count)

