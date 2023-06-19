from dataclasses import dataclass, field
from typing import List, Optional
from uuid import UUID

from sqlalchemy.engine import Row

from src.db.models import Item


@dataclass
class ItemDTO:
    id: UUID
    status: Item.ItemStatus
    sku: str
    barcode: str
    img: str
    count: int
    box_id: Optional[UUID] = None
    prompt: Optional[List[Optional[str]]] = field(default_factory=list)

    @classmethod
    def parse_from_db(cls, db_row: Row):
        return ItemDTO(
            id=db_row.id,
            status=db_row.status,
            sku=db_row.sku,
            barcode=db_row.barcode,
            img=db_row.img,
            count=db_row.count,
            box_id=db_row.box_id,
            prompt=[p.prompt for p in db_row.prompts],
        )
