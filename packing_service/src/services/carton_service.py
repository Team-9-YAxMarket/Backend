from fastapi import Depends

from src.db.models import Carton
from src.repository.carton_repository import CartonRepository


class CartonService:
    def __init__(
        self,
        carton_repository: CartonRepository = Depends(),
    ) -> None:
        self._carton_repository = carton_repository

    async def list_all_carton(self) -> list[Carton]:
        return await self._carton_repository.get_all()
