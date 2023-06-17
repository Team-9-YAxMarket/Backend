from typing import Any, List

from fastapi import Depends
from pydantic import PositiveInt
from src.repository.sku_cargo_repository import SKUCargotypeRepository
from src.repository.sku_repository import SKURepository
from src.api.request_models.request_base import SKURequest, SKUItemsRequest
from src.core.exceptions import SkuNotFoundError


class SKUService:
    """Сервис для работы с SKU."""

    def __init__(
        self,
        sku_repository: SKURepository = Depends(),
        sku_cargo_repository: SKUCargotypeRepository = Depends(),
    ) -> None:
        self.__sku_repository = sku_repository
        self.__sku_cargo_repository = sku_cargo_repository

    async def skus(self, sku: str, count: PositiveInt):
        """Возвращает статус о доступности отдельного sku из базы данных склада."""
        count_in_warehouse = await self.__sku_repository.get_sku_count(sku)
        if count_in_warehouse < count:
            return {"status": "FAULT"}
        return {"status": "OK"}

    async def all_skus(self, request: SKUItemsRequest):
        """Возвращает информацию о всех карготипах для sku из заказа."""
        response = []
        for item in request.items:
            sku_info = await self.__sku_repository.get_sku_info(item.sku)
            cargotypes_in_warehouse = (
                await self.__sku_cargo_repository.get_cargotypes_for_sku(
                    item.sku
                )
            )
            data = {
                "sku": item.sku,
                "length": sku_info.length,
                "width": sku_info.width,
                "height": sku_info.height,
                "weight": sku_info.weight,
                "barcode": sku_info.barcode,
                "img": sku_info.img,
                "cargotypes": cargotypes_in_warehouse
            }
            response.append(data)
        return {"items": response}

    async def all_skus_status(self, request: SKUItemsRequest):
        """Возвращает статус доступности на складе всех sku из заказа."""
        for item in request.items:
            count_in_warehouse = await self.__sku_repository.get_sku_count(
                item.sku
            )
            if count_in_warehouse < item.count:
                data = {"status": "FAULT"}
                return data
        return {"status": "OK"}
