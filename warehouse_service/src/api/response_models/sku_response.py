from typing import List

from pydantic import BaseModel, PositiveInt


class SKUResponseCount(BaseModel):
    sku: str
    count: PositiveInt

    class Config:
        orm_mode = True


class SKUResponse(BaseModel):
    status: str

    class Config:
        orm_mode = True


class SKUResponseItem(BaseModel):
    sku: str
    cargotypes: List[str]

    class Config:
        orm_mode = True


class SKUResponseItems(BaseModel):
    items: List[SKUResponseItem]

    class Config:
        orm_mode = True


class SKUResponseStatus(BaseModel):
    status: str
