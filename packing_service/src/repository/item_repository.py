from dataclasses import dataclass
from typing import List, Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from src.db.db import get_session
from src.db.models import Item
from src.repository.abstract_repository import AbstractRepository


@dataclass
class ItemDTO:
    id: UUID
    count: int
    sku: str
    barcode: str
    img: str


class ItemRepository(AbstractRepository):
    """Репозиторий для работы с моделью Item."""

    def __init__(self, session: AsyncSession = Depends(get_session)) -> None:
        super().__init__(session, Item)

    async def get_all_items(self) -> List[Optional[Item]]:
        stmt = select(Item).options(
            selectinload(Item.prompts),
        )
        items = await self._session.execute(stmt)
        return items.scalars().all()
