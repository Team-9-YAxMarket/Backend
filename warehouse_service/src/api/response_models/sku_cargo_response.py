from pydantic import BaseModel


class SKUCargoResponse(BaseModel):
    sku: str
    cargotype: int

    class Config:
        orm_mode = True

