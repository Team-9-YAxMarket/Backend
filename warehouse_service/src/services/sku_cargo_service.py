from typing import List

from warehouse_service.src.db.models import SKUCargotype
from warehouse_service.src.repository.sku_cargo_repository import (
    SKUCargotypeRepository,
)


class SKUCargoService:
    """Сервис для работы с SKU и их карготипами."""

    def __init__(self, sku_cargo_repository: SKUCargotypeRepository):
        self.sku_cargo_repository = sku_cargo_repository

    def list_all_skus(self) -> List[SKUCargotype]:
        return self.sku_cargo_repository.get_all()
