from pydantic import BaseModel, PositiveInt


class CartonResponse(BaseModel):
    carton_type: str
    barcode: str
    count: PositiveInt

    class Config:
        orm_mode = True
