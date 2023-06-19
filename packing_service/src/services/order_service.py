import uuid
from typing import Optional

from fastapi import Depends

from src.api.request_models.order_request import (
    OrderCreateRequest,
    OrderUpdateRequest,
)
from src.db.models import Order, RecommendedCarton
from src.repository.order_repository import OrderRepository
from src.services.carton_service import CartonService
from src.services.item_service import ItemService


class OrderService:
    def __init__(
        self,
        order_repository: OrderRepository = Depends(),
        carton_service: CartonService = Depends(),
        item_service: ItemService = Depends(),
    ) -> None:
        self._order_repository = order_repository
        self._carton_service = carton_service
        self._item_service = item_service

    async def get_next_order(self) -> Optional[Order]:
        return await self._order_repository.get_next_forming_order()

    async def get_order_by_id(self, order_id: uuid.UUID) -> Optional[Order]:
        return await self._order_repository.get(order_id)

    async def create_order(self, schema: OrderCreateRequest) -> Order:
        items = [await self._item_service.create_item(i) for i in schema.items]
        order = Order(items=items)
        return await self._order_repository.create(order)

    async def update_order(
        self, order_id: uuid.UUID, schema: OrderUpdateRequest
    ) -> Order:
        order: Order = await self._order_repository.get(order_id)
        box_id: Optional[uuid.UUID] = None

        # Update recommended carton
        if schema.package:
            box_id = uuid.uuid4()
            recommended_carton = RecommendedCarton(box_id=box_id)
            recommended_carton.carton = (
                await self._carton_service.get_carton_by_carton_type(
                    schema.package
                )
            )
            order.recommended_carton = [recommended_carton]

        # Update items without carton recommendation
        for schema_item in schema.no_room_for:
            item = await self._item_service.get_by_order_and_sku(
                order.id, schema_item.sku
            )
            await self._item_service.update_item(item, schema_item)

        # Update items with carton recommendation
        for schema_item in schema.items:
            item = await self._item_service.get_by_order_and_sku(
                order.id, schema_item.sku
            )
            if box_id:
                item.box_id = box_id
            await self._item_service.update_item(item, schema_item)

        return await self._order_repository.update(order)
