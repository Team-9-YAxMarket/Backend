from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi_restful.cbv import cbv
from starlette.responses import JSONResponse

from src.api.dto.session_dto import SessionDTO
from src.api.request_models.session_request import (
    SessionCreateRequest,
    SessionUpdateRequest,
)
from src.api.response_models.session_response import (
    SessionCreateResponse,
    SessionFullResponse,
    SessionUpdateResponse,
)
from src.core.tools import generate_error_responses
from src.services.session_service import SessionService

router = APIRouter(prefix="/session", tags=["Session"])


@cbv(router)
class SessionCBV:
    _session_service: SessionService = Depends()

    @router.post(
        "/",
        response_model=SessionCreateResponse,
        response_model_exclude_none=False,
        status_code=HTTPStatus.CREATED,
        summary="Create new user session",
        response_description=HTTPStatus.CREATED.phrase,
        responses=generate_error_responses(HTTPStatus.BAD_REQUEST),
    )
    async def create_session(
        self, session: SessionCreateRequest
    ) -> SessionCreateResponse:
        session = await self._session_service.create_session(session)
        if not session:
            return JSONResponse({})
        return SessionDTO.parse_from_db(session)

    @router.get(
        "/{session_id}",
        response_model=SessionFullResponse,
        response_model_exclude_none=False,
        status_code=HTTPStatus.OK,
        summary="Get user session",
        response_description=HTTPStatus.OK.phrase,
        responses=generate_error_responses(
            HTTPStatus.BAD_REQUEST, HTTPStatus.NOT_FOUND
        ),
    )
    async def get_session(self, session_id: UUID) -> SessionFullResponse:
        session = await self._session_service.get_session(session_id)
        return SessionDTO.parse_from_db(session)

    @router.patch(
        "/{session_id}",
        response_model=SessionUpdateResponse,
        response_model_exclude_none=False,
        status_code=HTTPStatus.OK,
        summary="Update user session",
        response_description=HTTPStatus.OK.phrase,
        responses=generate_error_responses(
            HTTPStatus.BAD_REQUEST, HTTPStatus.NOT_FOUND
        ),
    )
    async def close_session(
        self, session_id: UUID, session: SessionUpdateRequest
    ) -> SessionUpdateResponse:
        session = await self._session_service.close_session(
            session_id, session
        )
        return SessionDTO.parse_from_db(session)
