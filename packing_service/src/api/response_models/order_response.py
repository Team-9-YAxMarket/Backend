from datetime import datetime
from typing import List, Optional

from pydantic import UUID4, BaseModel

from src.api.response_models.carton_response import CartonResponse
from src.api.response_models.item_response import ItemResponse
from src.db.models import Order


class OrderCreateResponse(BaseModel):
    id: UUID4

    class Config:
        orm_mode = True


class OrderGetResponse(BaseModel):
    order_id: UUID4
    recommended_carton: List[Optional[CartonResponse]]
    items: List[ItemResponse]

    class Config:
        orm_mode = True
