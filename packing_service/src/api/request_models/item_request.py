from typing import List, Optional

from pydantic import UUID4, AnyUrl, BaseModel, PositiveInt

from src.db.models import Item


class ItemCreateRequest(BaseModel):
    sku: str
    barcode: str
    img: AnyUrl
    count: PositiveInt


class ItemUpdateRequest(BaseModel):
    sku: str
    add_packs: List[Optional[str]] | None = []


class ItemSessionCloseRequest(BaseModel):
    id: UUID4
    status: Item.ItemStatus
