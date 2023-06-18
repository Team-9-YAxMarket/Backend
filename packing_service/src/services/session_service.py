from datetime import datetime
from uuid import UUID

from fastapi import Depends

from src.api.request_models.session_request import (
    SessionCreateRequest,
    SessionUpdateRequest,
)
from src.db.models import Session, Order
from src.repository.session_repository import SessionRepository
from src.services.carton_service import CartonService
from src.services.order_service import OrderService


class SessionService:
    def __init__(
        self,
        session_repository: SessionRepository = Depends(),
        order_service: OrderService = Depends(),
        carton_service: CartonService = Depends(),
    ) -> None:
        self._session_repository = session_repository
        self._order_service = order_service
        self._carton_service = carton_service

    async def create_session(self, schema: SessionCreateRequest) -> Session:
        session = Session(user_id=schema.user_id)
        order = await self._order_service.get_next_order()
        if not order:
            return None
        order.status = Order.OrderStatus.IS_COLLECTING
        session.order = order
        return await self._session_repository.create(session)

    async def get_session(self, session_id: UUID) -> Session:
        return await self._session_repository.get(session_id)

    async def close_session(
        self, session_id: UUID, schema: SessionUpdateRequest
    ) -> Session:
        session = await self._session_repository.get(session_id)

        # Update session status
        session.status = schema.status

        # Update order status
        if schema.status is Session.SessionStatus.CLOSED_SUCCESS:
            session.order.status = Order.OrderStatus.IS_READY

        # Update selected carton
        if schema.order.selected_carton:
            session.order.selected_carton = [
                await self._carton_service.get_carton_by_id(c)
                for c in schema.order.selected_carton
            ]

        # Update item status
        item_status = {i.id: i.status for i in schema.order.items}
        for item in session.order.items:
            item.status = item_status[item.id]

        # Update session close time
        session.end_at = datetime.utcnow()

        return await self._session_repository.update(session)
