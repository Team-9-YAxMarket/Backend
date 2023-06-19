from decimal import Decimal
from typing import List

from pydantic import AnyUrl, BaseModel, PositiveInt


class SKUResponse(BaseModel):
    status: str

    class Config:
        orm_mode = True


class SKUResponseItem(BaseModel):
    sku: str
    length: Decimal
    width: Decimal
    height: Decimal
    weight: Decimal
    barcode: str
    count: PositiveInt
    img: AnyUrl
    cargotypes: List[str]

    class Config:
        orm_mode = True


class SKUResponseItems(BaseModel):
    items: List[SKUResponseItem]

    class Config:
        orm_mode = True


class SKUResponseStatus(BaseModel):
    status: str
