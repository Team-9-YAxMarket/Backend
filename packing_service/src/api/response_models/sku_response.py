from pydantic import UUID4, AnyUrl, BaseModel


class SKUResponse(BaseModel):
    id: UUID4
    sku: str
    barcode: str
    img: AnyUrl

    class Config:
        orm_mode = True
