from typing import Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.db import get_session
from src.db.models import Prompt
from src.repository.abstract_repository import AbstractRepository


class PromptRepository(AbstractRepository):
    """Репозиторий для работы с моделью Prompt."""

    def __init__(self, session: AsyncSession = Depends(get_session)) -> None:
        super().__init__(session, Prompt)

    async def get_prompt_by_name_or_none(
        self, prompt: str
    ) -> Optional[Prompt]:
        prompt = await self._session.execute(
            select(Prompt).where(Prompt.prompt == prompt)
        )
        return prompt.scalars().first()
