from pydantic import BaseModel, Extra
from decimal import Decimal
from uuid import UUID
from typing import List
from pydantic import BaseModel, Extra, Field, NonNegativeInt, condecimal


class RequestBase(BaseModel):
    """Request model base class.

    It is forbidden to have fields not provided for by the scheme."""

    class Config:
        extra = Extra.forbid


class SKURequest(RequestBase):
    sku: str
    count: int


class SKUItemsRequest(RequestBase):
    items: List[SKURequest]


