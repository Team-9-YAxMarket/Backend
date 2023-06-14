from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends
from fastapi_restful.cbv import cbv

from src.api.request_models.prompt_request import PromptRequest
from src.api.response_models.prompt_response import PromptResponse
from src.core.tools import generate_error_responses
from src.services.prompt_service import PromptService

router = APIRouter(prefix="/prompt", tags=["Prompt"])


@cbv(router)
class UserCBV:
    _prompt_service: PromptService = Depends()

    @router.get(
        "/",
        response_model=List[PromptResponse],
        response_model_exclude_none=True,
        status_code=HTTPStatus.OK,
        summary="Get Prompt list",
        response_description=HTTPStatus.OK.phrase,
    )
    async def list_prompts(self) -> List[PromptResponse]:
        return await self._prompt_service.list_all_prompt()

    @router.post(
        "/",
        response_model=PromptResponse,
        response_model_exclude_none=True,
        status_code=HTTPStatus.OK,
        summary="Create prompt",
        response_description=HTTPStatus.OK.phrase,
        responses=generate_error_responses(HTTPStatus.BAD_REQUEST),
    )
    async def create_prompt(self, prompt: PromptRequest) -> PromptResponse:
        return await self._prompt_service.create_or_get_prompt(prompt.prompt)
