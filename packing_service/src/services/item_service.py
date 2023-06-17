from typing import List
from uuid import UUID

from fastapi import Depends

from src.api.request_models.item_request import (
    ItemCreateRequest,
    ItemUpdateRequest,
)
from src.db.models import Item
from src.repository.item_repository import ItemRepository
from src.services.prompt_service import PromptService


class ItemService:
    def __init__(
        self,
        item_repository: ItemRepository = Depends(),
        prompt_service: PromptService = Depends(),
    ) -> None:
        self._item_repository = item_repository
        self._prompt_service = prompt_service

    async def create_item(self, schema: ItemCreateRequest) -> Item:
        return await self._item_repository.create(Item(**schema.dict()))

    async def list_all_items(self) -> List[Item]:
        items = await self._item_repository.get_all_items()
        return items

    async def get_by_order_and_sku(self, order_id: UUID, sku: str) -> Item:
        return await self._item_repository.get_by_order_and_sku(order_id, sku)

    async def update_item(self, item: Item, schema: ItemUpdateRequest) -> Item:
        if schema.add_packs:
            prompts = [
                await self._prompt_service.create_or_get_prompt(p)
                for p in schema.add_packs
            ]
            item.prompts = prompts

        return await self._item_repository.update(item)
