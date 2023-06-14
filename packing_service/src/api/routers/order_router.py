from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends
from fastapi_restful.cbv import cbv

from src.api.request_models.order_request import OrderCreateRequest
from src.api.response_models.order_response import (
    OrderCreateResponse,
    OrderGetResponse,
)
from src.core.tools import generate_error_responses
from src.services.order_service import OrderService

router = APIRouter(prefix="/order", tags=["Order"])


@cbv(router)
class UserCBV:
    _order_service: OrderService = Depends()

    @router.get(
        "/",
        response_model=List[OrderGetResponse],
        response_model_exclude_none=True,
        status_code=HTTPStatus.OK,
        summary="Get Order list",
        response_description=HTTPStatus.OK.phrase,
    )
    async def list_orders(self) -> List[OrderGetResponse]:
        return await self._order_service.list_all_orders()

    @router.post(
        "/",
        response_model=OrderCreateResponse,
        response_model_exclude_none=True,
        status_code=HTTPStatus.OK,
        summary="Create order",
        response_description=HTTPStatus.OK.phrase,
        responses=generate_error_responses(HTTPStatus.BAD_REQUEST),
    )
    async def create_order(
        self, order: OrderCreateRequest
    ) -> OrderCreateResponse:
        order_obj = await self._order_service.create_order(order)
        print("*" * 100)
        print(order_obj)
        print("*" * 100)
        return order_obj
