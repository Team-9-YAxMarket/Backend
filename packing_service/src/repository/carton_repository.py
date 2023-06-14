from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.db import get_session
from src.db.models import Carton
from src.repository.abstract_repository import AbstractRepository


class CartonRepository(AbstractRepository):
    """Репозиторий для работы с моделью Carton."""

    def __init__(self, session: AsyncSession = Depends(get_session)) -> None:
        super().__init__(session, Carton)
