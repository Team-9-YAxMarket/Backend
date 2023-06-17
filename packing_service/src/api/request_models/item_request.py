from typing import List, Optional

from pydantic import AnyUrl, BaseModel, PositiveInt


class ItemCreateRequest(BaseModel):
    sku: str
    barcode: str
    img: AnyUrl
    count: PositiveInt


class ItemUpdateRequest(BaseModel):
    sku: str
    add_packs: List[Optional[str]]
