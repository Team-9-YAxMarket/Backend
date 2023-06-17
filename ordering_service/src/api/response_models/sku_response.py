from decimal import Decimal
from typing import List

from pydantic import AnyUrl, BaseModel, PositiveInt


class SKUResponseStatus(BaseModel):
    status: str


class SKUResponseItem(BaseModel):
    sku: str
    length: Decimal
    width: Decimal
    height: Decimal
    weight: Decimal
    barcode: str
    img: AnyUrl
    cargotypes: List[str]


class SKUResponseList(BaseModel):
    items: List[SKUResponseItem]

