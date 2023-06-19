from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends
from fastapi_restful.cbv import cbv

from src.api.response_models.sku_response import SKUResponse, SKUResponseStatus

from src.api.request_models.request_base import SKUItemsRequestStatus

from src.services.sku_service import SKUService

from src.api.response_models.sku_response import SKUResponseItems


router_sku = APIRouter(prefix="/check_skus", tags=["SKU"])


@cbv(router_sku)
class SKUCBV:
    __sku_service: SKUService = Depends()

    @router_sku.post(
        "/",
        response_model=SKUResponseItems,
        response_model_exclude_none=True,
        status_code=HTTPStatus.OK,
        summary="Checking presence of SKUs",
        response_description=HTTPStatus.OK.phrase,
    )
    async def check_all_skus(
        self, request: SKUItemsRequestStatus
    ) -> Optional[SKUResponseItems]:
        return await self.__sku_service.all_skus(request)

    @router_sku.post(
        "/status/",
        response_model=SKUResponseStatus,
        response_model_exclude_none=True,
        status_code=HTTPStatus.OK,
        summary="Checking presence of SKUs",
        response_description=HTTPStatus.OK.phrase,
    )
    async def check_all_skus_status(
        self, request: SKUItemsRequestStatus
    ) -> Optional[SKUResponseStatus]:
        return await self.__sku_service.all_skus_status(request)
