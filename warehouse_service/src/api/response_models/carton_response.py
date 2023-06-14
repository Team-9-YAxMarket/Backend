from pydantic import BaseModel
from decimal import Decimal


class CartonResponse(BaseModel):
    carton_type: str
    length: Decimal
    width: Decimal
    height: Decimal
    barcode: str
    in_stock: int

    class Config:
        orm_mode = True
