from pydantic import UUID4, AnyUrl, BaseModel


class SKURequest(BaseModel):
    id: UUID4
    sku: str
    barcode: str
    img: AnyUrl
