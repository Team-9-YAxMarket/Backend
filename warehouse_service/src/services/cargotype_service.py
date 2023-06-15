from typing import List

from warehouse_service.src.api.response_models.cargotype_response import (
    CargotypeResponse,
)
from warehouse_service.src.core.exceptions import CargotypeNotFoundError
from warehouse_service.src.db.models import Cargotype
from warehouse_service.src.repository.cargotype_repository import (
    CargotypeRepository,
)


class CargotypeService:
    def __init__(self, cargotype_repository: CargotypeRepository):
        self.cargotype_repository = cargotype_repository

    def list_all_cargotypes(self) -> List[Cargotype]:
        return self.cargotype_repository.get_all()

    def create_cargotype(self, cargotype_data: CargotypeResponse) -> Cargotype:
        cargotype = Cargotype(**cargotype_data.dict())
        return self.cargotype_repository.create(cargotype)

    def delete_cargotype(self, cargotype_id: int):
        cargotype = self.cargotype_repository.get_by_id(cargotype_id)
        if not cargotype:
            raise CargotypeNotFoundError
        self.cargotype_repository.delete(cargotype)

    def update_cargotype(
        self, cargotype_id: int, cargotype_data: CargotypeResponse
    ) -> Cargotype:
        cargotype = self.cargotype_repository.get_by_id(cargotype_id)
        if not cargotype:
            raise CargotypeNotFoundError
        cargotype.cargotype = cargotype_data.cargotype
        cargotype.description = cargotype_data.description
        return self.cargotype_repository.update(cargotype)
