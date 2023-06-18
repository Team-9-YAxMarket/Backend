import decimal
from typing import List
from pydantic import BaseModel, Extra, PositiveInt


class RequestBase(BaseModel):
    """Request model base class.

    It is forbidden to have fields not provided for by the scheme."""

    class Config:
        extra = Extra.forbid


# class SKURequest(RequestBase):
#     sku: str
#     count: PositiveInt
#
#
# class SKUItemsRequest(RequestBase):
#     items: List[SKURequest]
#

class SKURequestStatus(RequestBase):
    sku: str
    count: PositiveInt


class SKUItemsRequestStatus(RequestBase):
    items: List[SKURequestStatus]


