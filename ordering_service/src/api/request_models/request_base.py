from typing import List
from pydantic import BaseModel, Extra, PositiveInt


class RequestBase(BaseModel):
    """Request model base class.

    It is forbidden to have fields not provided for by the scheme."""

    class Config:
        extra = Extra.forbid


class SKURequest(BaseModel):
    sku: str


class ItemRequest(BaseModel):
    sku: str
    count: PositiveInt


class OrderRequest(BaseModel):
    items: List[ItemRequest]
