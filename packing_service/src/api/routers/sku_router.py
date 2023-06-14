from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends
from fastapi_restful.cbv import cbv

from src.api.request_models.sku_request import SKURequest
from src.api.response_models.sku_response import SKUResponse
from src.core.tools import generate_error_responses
from src.services.sku_service import SKUService

router = APIRouter(prefix="/sku", tags=["SKU"])


@cbv(router)
class UserCBV:
    _sku_service: SKUService = Depends()

    @router.get(
        "/",
        response_model=List[SKUResponse],
        response_model_exclude_none=True,
        status_code=HTTPStatus.OK,
        summary="Get SKU list",
        response_description=HTTPStatus.OK.phrase,
    )
    async def list_skus(self) -> List[SKUResponse]:
        return await self._sku_service.list_all_sku()

    @router.post(
        "/",
        response_model=SKUResponse,
        response_model_exclude_none=True,
        status_code=HTTPStatus.OK,
        summary="Create sku",
        response_description=HTTPStatus.OK.phrase,
        responses=generate_error_responses(HTTPStatus.BAD_REQUEST),
    )
    async def create_sku(self, sku: SKURequest) -> SKUResponse:
        return await self._sku_service.create_or_get_sku(sku)
