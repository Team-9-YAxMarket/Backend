from http import HTTPStatus
from typing import Any

from fastapi import APIRouter, Depends
from fastapi_restful.cbv import cbv

from src.api.response_models.user_response import UserResponse
from src.core.tools import generate_error_responses
from src.services.session_service import SessionService

router = APIRouter(prefix="/user", tags=["User"])


@cbv(router)
class UserCBV:
    _session_service: SessionService = Depends()

    @router.get(
        "/",
        response_model=UserResponse,
        response_model_exclude_none=True,
        status_code=HTTPStatus.OK,
        summary="Create new user",
        response_description=HTTPStatus.OK.phrase,
        responses=generate_error_responses(HTTPStatus.BAD_REQUEST),
    )
    async def add_user(self) -> Any:
        return await self._session_service.list_all_sessions()
