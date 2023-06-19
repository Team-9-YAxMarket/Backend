from typing import List, Optional

from pydantic import UUID4, BaseModel, Field

from src.api.request_models.item_request import (
    ItemCreateRequest,
    ItemSessionCloseRequest,
    ItemUpdateRequest,
)


class OrderCreateRequest(BaseModel):
    items: List[ItemCreateRequest]


class OrderUpdateRequest(BaseModel):
    id: UUID4 = Field(alias="orderId")
    package: Optional[str]
    items: List[Optional[ItemUpdateRequest]]
    no_room_for: List[Optional[ItemUpdateRequest]]


class OrderSessionCloseRequest(BaseModel):
    order_id: UUID4
    selected_carton: List[str]
    items: List[ItemSessionCloseRequest]
