from dataclasses import dataclass
from typing import List, Optional
from uuid import UUID

from sqlalchemy.engine import Row

from src.api.dto.carton_dto import CartonDTO
from src.api.dto.item_dto import ItemDTO


@dataclass
class OrderDTO:
    order_id: UUID
    recommended_carton: List[Optional[CartonDTO]]
    items: List[ItemDTO]

    @classmethod
    def parse_from_db(cls, db_row: Row):
        return OrderDTO(
            order_id=db_row.id,
            recommended_carton=[
                CartonDTO(r) for r in db_row.recommended_carton
            ],
            items=[ItemDTO.parse_from_db(i) for i in db_row.items],
        )
