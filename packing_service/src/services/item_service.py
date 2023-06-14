from typing import List

from fastapi import Depends

from src.api.request_models.item_request import ItemRequest
from src.db.models import Item
from src.repository.item_repository import ItemRepository
from src.services.prompt_service import PromptService
from src.services.sku_service import SKUService


class ItemService:
    def __init__(
        self,
        item_repository: ItemRepository = Depends(),
        sku_service: SKUService = Depends(),
        prompt_serivce: PromptService = Depends(),
    ) -> None:
        self._item_repository = item_repository
        self._sku_service = sku_service
        self._prompt_service = prompt_serivce

    async def list_all_item(self) -> List[Item]:
        return await self._item_repository.get_all()

    async def create_item(self, schema: ItemRequest) -> Item:
        sku = await self._sku_service.create_or_get_sku(schema.sku)
        prompts = [
            await self._prompt_service.create_or_get_prompt(p)
            for p in schema.prompts or []
        ]
        schema_dict = schema.dict()
        schema_dict["sku"] = sku
        schema_dict["prompts"] = prompts

        return await self._item_repository.create(Item(**schema_dict))
