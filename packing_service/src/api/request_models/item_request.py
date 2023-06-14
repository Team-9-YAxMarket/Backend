from typing import List, Optional

from pydantic import UUID4, BaseModel, PositiveInt

from src.api.request_models.prompt_request import PromptRequest
from src.api.request_models.sku_request import SKURequest


class ItemRequest(BaseModel):
    sku: SKURequest
    count: PositiveInt
    prompts: Optional[List[Optional[str]]]
    box_id: Optional[UUID4]
