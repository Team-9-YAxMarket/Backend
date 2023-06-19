from typing import Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.db import get_session
from src.db.models import Order
from src.repository.abstract_repository import AbstractRepository


class OrderRepository(AbstractRepository):
    """Репозиторий для работы с моделью Order."""

    def __init__(self, session: AsyncSession = Depends(get_session)) -> None:
        super().__init__(session, Order)

    async def get_next_forming_order(self) -> Optional[Order]:
        stmt = (
            select(Order)
            .where(Order.status == Order.OrderStatus.IS_FORMING)
            .order_by(Order.updated_at)
        )
        order = (await self._session.execute(stmt)).scalars().first()
        if not order:
            return None
        return order
