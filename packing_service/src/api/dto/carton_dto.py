from dataclasses import dataclass
from typing import List, Optional
from uuid import UUID

from sqlalchemy.engine import Row


@dataclass
class CartonDTO:
    carton_id: UUID
    carton_type: str
    barcode: str
    box_id: Optional[UUID]

    @classmethod
    def parse_from_db(cls, db_row: Row):
        return CartonDTO(
            carton_id=db_row.id,
            carton_type=db_row.carton_type,
            barcode=db_row.barcode,
            box_id=db_row.box_id,
        )
