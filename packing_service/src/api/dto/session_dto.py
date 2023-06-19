from dataclasses import dataclass
from uuid import UUID

from sqlalchemy.engine import Row

from src.api.dto.order_dto import OrderDTO
from src.db.models import Order


@dataclass
class SessionDTO:
    session_id: UUID
    user_id: UUID
    status: Order.OrderStatus
    order: OrderDTO

    @classmethod
    def parse_from_db(cls, db_row: Row):
        return SessionDTO(
            session_id=db_row.id,
            user_id=db_row.user_id,
            status=db_row.status,
            order=OrderDTO.parse_from_db(db_row.order),
        )
