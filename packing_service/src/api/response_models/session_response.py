from pydantic import UUID4, BaseModel

from src.api.response_models.order_response import OrderGetResponse
from src.db.models import Session


class SessionCreateResponse(BaseModel):
    session_id: UUID4
    user_id: UUID4
    order: OrderGetResponse

    class Config:
        orm_mode = True


class SessionUpdateResponse(BaseModel):
    session_id: UUID4
    user_id: UUID4
    status: Session.SessionStatus

    class Config:
        orm_mode = True
