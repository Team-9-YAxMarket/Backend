from typing import Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.db import get_session
from src.db.models import Item
from src.repository.abstract_repository import AbstractRepository


class ItemRepository(AbstractRepository):
    """Репозиторий для работы с моделью Item."""

    def __init__(self, session: AsyncSession = Depends(get_session)) -> None:
        super().__init__(session, Item)
