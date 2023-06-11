from fastapi import Depends

from src.db.models import Session
from src.repository.session_repository import SessionRepository


class SessionService:
    def __init__(
        self,
        session_repository: SessionRepository = Depends(),
    ) -> None:
        self.__session_repository = session_repository

    async def list_all_sessions(self) -> list[Session]:
        return await self.__session_repository.get_all()
