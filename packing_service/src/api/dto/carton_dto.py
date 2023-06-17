from dataclasses import dataclass
from typing import Optional
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
            carton_id=db_row.carton.id,
            carton_type=db_row.carton.carton_type,
            barcode=db_row.carton.barcode,
            box_id=db_row.box_id,
        )
