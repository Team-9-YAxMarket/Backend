from typing import List

from fastapi import Depends

from src.api.request_models.prompt_request import PromptRequest
from src.db.models import Prompt
from src.repository.prompt_repository import PromptRepository


class PromptService:
    def __init__(
        self,
        prompt_repository: PromptRepository = Depends(),
    ) -> None:
        self._prompt_repository = prompt_repository

    async def list_all_prompt(self) -> List[Prompt]:
        return await self._prompt_repository.get_all()

    async def create_or_get_prompt(self, schema: PromptRequest) -> Prompt:
        prompt = await self._prompt_repository.get_prompt_by_name_or_none(
            schema.prompt
        ) or await self._prompt_repository.create(Prompt(**schema.dict()))

        return prompt
