from http import HTTPStatus
from typing import Any, List

from fastapi import APIRouter, Depends
from fastapi_restful.cbv import cbv

from src.api.response_models.carton_response import CartonResponse
from src.services.carton_service import CartonService

router = APIRouter(prefix="/carton", tags=["Carton"])


@cbv(router)
class CartonCBV:
    _carton_service: CartonService = Depends()

    @router.get(
        "/",
        response_model=List[CartonResponse],
        response_model_exclude_none=True,
        status_code=HTTPStatus.OK,
        summary="Get Carton list",
        response_description=HTTPStatus.OK.phrase,
    )
    async def list_carton(self) -> CartonResponse:
        return await self._carton_service.list_all_carton()
