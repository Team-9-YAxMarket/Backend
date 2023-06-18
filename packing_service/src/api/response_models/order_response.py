from typing import List, Optional

from pydantic import UUID4, BaseModel, Field

from src.api.response_models.carton_response import CartonAsPartResponse
from src.api.response_models.item_response import ItemFullResponse


class OrderCreateResponse(BaseModel):
    orderId: UUID4 = Field(alias="id")  # noqa N815

    class Config:
        orm_mode = True


class OrderGetResponse(BaseModel):
    order_id: UUID4
    recommended_carton: List[Optional[CartonAsPartResponse]]
    items: List[ItemFullResponse]

    class Config:
        orm_mode = True


class OrderUpdateResponse(BaseModel):
    id: UUID4

    class Config:
        orm_mode = True
