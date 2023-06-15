from typing import List, Optional

from pydantic import UUID4, AnyUrl, BaseModel, PositiveInt


class ItemRequest(BaseModel):
    sku: str
    barcode: str
    img: AnyUrl
    count: PositiveInt
    prompts: Optional[List[Optional[str]]]
    box_id: Optional[UUID4]
