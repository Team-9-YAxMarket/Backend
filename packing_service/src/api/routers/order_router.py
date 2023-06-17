from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends
from fastapi_restful.cbv import cbv

from src.api.request_models.order_request import (
    OrderCreateRequest,
    OrderUpdateRequest,
)
from src.api.response_models.order_response import (
    OrderCreateResponse,
    OrderGetResponse,
    OrderUpdateResponse,
)
from src.core.tools import generate_error_responses
from src.services.order_service import OrderService

router = APIRouter(prefix="/order", tags=["Order"])


@cbv(router)
class UserCBV:
    _order_service: OrderService = Depends()

    @router.get(
        "/",
        response_model=Optional[OrderGetResponse],
        response_model_exclude_none=True,
        status_code=HTTPStatus.OK,
        summary="Get Order list",
        response_description=HTTPStatus.OK.phrase,
    )
    async def get_next_order(self) -> Optional[OrderGetResponse]:
        return await self._order_service.get_next_order()

    @router.post(
        "/",
        response_model=OrderCreateResponse,
        response_model_by_alias=False,
        response_model_exclude_none=True,
        status_code=HTTPStatus.CREATED,
        summary="Create order",
        response_description=HTTPStatus.CREATED.phrase,
        responses=generate_error_responses(HTTPStatus.BAD_REQUEST),
    )
    async def create_order(
        self, order: OrderCreateRequest
    ) -> OrderCreateResponse:
        return await self._order_service.create_order(order)

    @router.patch(
        "/",
        response_model=OrderUpdateResponse,
        response_model_exclude_none=True,
        status_code=HTTPStatus.OK,
        summary="Update order",
        response_description=HTTPStatus.OK.phrase,
        responses=generate_error_responses(HTTPStatus.BAD_REQUEST),
    )
    async def update_order(
        self, order: OrderUpdateRequest
    ) -> OrderUpdateResponse:
        order = await self._order_service.update_order(order)
        return order
