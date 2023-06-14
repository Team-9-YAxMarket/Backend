from typing import List

from pydantic import BaseModel

from src.api.response_models.cargotype_response import CargotypeResponse


class SKUResponse(BaseModel):
    sku: str
    cargotype: List[int]

    class Config:
        orm_mode = True


class SKUResponseDeny(BaseModel):
    status: str
