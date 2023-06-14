from typing import Optional

from pydantic import UUID4, BaseModel


class CartonResponse(BaseModel):
    id: UUID4
    carton_type: str
    barcode: str
    box_id: Optional[UUID4]

    class Config:
        orm_mode = True
