from typing import List

from fastapi import Depends

from src.api.request_models.sku_request import SKURequest
from src.db.models import SKU
from src.repository.sku_repository import SKURepository


class SKUService:
    def __init__(
        self,
        sku_repository: SKURepository = Depends(),
    ) -> None:
        self._sku_repository = sku_repository

    async def list_all_sku(self) -> List[SKU]:
        return await self._sku_repository.get_all()

    async def create_or_get_sku(self, schema: SKURequest) -> SKU:
        sku = await self._sku_repository.get_sku_by_name_or_none(
            schema.sku
        ) or await self._sku_repository.create(SKU(**schema.dict()))

        return sku
