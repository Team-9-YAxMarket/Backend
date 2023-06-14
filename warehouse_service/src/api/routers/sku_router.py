from http import HTTPStatus
from typing import Any, List, Union
from uuid import UUID

from fastapi import APIRouter, Depends , Request
from fastapi_restful.cbv import cbv
from sqlalchemy import column, select, table

from src.api.response_models.sku_response import SKUResponse
from src.db.db import get_session
from src.db.models import SKU

from src.api.response_models.sku_response import SKUResponseDeny

from src.api.request_models.request_base import SKUItemsRequest, SKURequest

# from src.repository.sku_repository import SKURepository

from src.services.sku_service import SKUService

router_sku = APIRouter(prefix="/check_skus", tags=["SKU"])


@cbv(router_sku)
class SKUCBV:
    __sku_service: SKUService = Depends()

    @router_sku.post(
        "/",
        response_model=SKUResponse,
        response_model_exclude_none=True,
        status_code=HTTPStatus.OK,
        summary="Checking presence of SKUs",
        response_description=HTTPStatus.OK.phrase,
    )
    async def check_skus(self, request: Request):
        data = await request.json()
        items = SKUItemsRequest(**data)
        response = []
        for item in items:
            _, req_item = item
            response_dict = {}
            # order_item = SKURequest(**req_item)
            cargotypes = await self.__sku_service.cargotypes(req_item.sku, req_item.count)
            response_dict['sku'] = req_item.sku
            response_dict['cargotypes'] = cargotypes
            response.append(response_dict)
        return response

