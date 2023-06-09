from fastapi import Depends

from src.db.models import User
from src.repository.user_repository import UserRepository


class UserService:
    def __init__(
        self,
        user_repository: UserRepository = Depends(),
    ) -> None:
        self.__user_repository = user_repository

    async def list_all_users(self) -> list[User]:
        return await self.__user_repository.get_all_users()
