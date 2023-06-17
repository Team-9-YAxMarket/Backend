from typing import List, Optional

from pydantic import UUID4, AnyUrl, BaseModel, PositiveInt


class ItemResponse(BaseModel):
    id: UUID4
    sku: str
    barcode: str
    img: AnyUrl
    count: PositiveInt
    box_id: Optional[UUID4]

    class Config:
        orm_mode = True


class ItemFullResponse(BaseModel):
    id: UUID4
    sku: str
    barcode: str
    img: AnyUrl
    count: PositiveInt
    prompt: List[Optional[str]]
    box_id: Optional[UUID4]

    class Config:
        orm_mode = True
