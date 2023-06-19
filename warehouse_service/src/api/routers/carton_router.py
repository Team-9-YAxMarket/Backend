from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends
from fastapi_restful.cbv import cbv
from src.services.carton_service import CartonService

from src.api.response_models.carton_response import CartonResponse

router_carton = APIRouter(prefix="/check_carton", tags=["Carton"])


@cbv(router_carton)
class CartonCBV:
    __carton_service: CartonService = Depends()

    @router_carton.get(
        "/",
        response_model=CartonResponse,
        response_model_exclude_none=True,
        status_code=HTTPStatus.OK,
        summary="Checking presence of Carton",
        response_description=HTTPStatus.OK.phrase,
    )
    async def check_carton(self, carton_type: str) -> Optional[CartonResponse]:
        return await self.__carton_service.cartons_info(carton_type)
