from pydantic import UUID4, BaseModel


class CartonResponse(BaseModel):
    id: UUID4
    carton_type: str
    barcode: str

    class Config:
        orm_mode = True
