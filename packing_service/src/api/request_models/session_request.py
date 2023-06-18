from pydantic import BaseModel, UUID4
from src.api.request_models.order_request import OrderSessionCloseRequest
from src.db.models import Session


class SessionCreateRequest(BaseModel):
    user_id: UUID4


class SessionUpdateRequest(BaseModel):
    session_id: UUID4
    user_id: str
    status: Session.SessionStatus
    order: OrderSessionCloseRequest
