from typing import List

from fastapi import Depends

from src.api.request_models.item_request import ItemRequest
from src.db.models import Item
from src.repository.item_repository import ItemRepository
from src.services.prompt_service import PromptService


class ItemService:
    def __init__(
        self,
        item_repository: ItemRepository = Depends(),
        prompt_serivce: PromptService = Depends(),
    ) -> None:
        self._item_repository = item_repository
        self._prompt_service = prompt_serivce

    async def list_all_items(self) -> List[Item]:
        items = await self._item_repository.get_all_items()
        print("+" * 100)
        print(*[item.prompts for item in items], sep="\n")
        print("+" * 100)
        return items

    async def create_item(self, schema: ItemRequest) -> Item:
        if schema.prompts is None:
            prompts = []
        else:
            prompts = [
                await self._prompt_service.create_or_get_prompt(p)
                for p in schema.prompts
            ]
        schema_dict = schema.dict()
        schema_dict["prompts"] = prompts
        return await self._item_repository.create(Item(**schema_dict))
