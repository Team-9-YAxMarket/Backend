from fastapi import Depends
from pydantic import PositiveInt
from src.repository.carton_repository import CartonRepository
from src.api.response_models.carton_response import CartonResponse
from src.core.exceptions import CartonNotFoundError


class CartonService:
    """Сервис для работы с моделью Carton."""

    def __init__(
        self, carton_repository: CartonRepository = Depends()
    ) -> None:
        self.__carton_repository = carton_repository

    async def cartons_info(self, carton_type: str, count: PositiveInt):
        """Возвращает информацию о доступных упаковках из базы данных склада."""
        carton = await self.__carton_repository.get_carton(carton_type)
        if carton is None or carton.count < count:
            raise CartonNotFoundError(carton_type)
        return CartonResponse(
            carton_type=carton.carton_type,
            barcode=carton.barcode,
            count=carton.count,
        )
