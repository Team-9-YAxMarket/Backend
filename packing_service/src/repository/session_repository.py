from uuid import UUID

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core import exceptions
from src.db.db import get_session
from src.db.models import Session
from src.repository.abstract_repository import AbstractRepository


class SessionRepository(AbstractRepository):
    """Репозиторий для работы с моделью User."""

    def __init__(self, session: AsyncSession = Depends(get_session)) -> None:
        super().__init__(session, Session)
