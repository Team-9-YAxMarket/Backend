from pydantic import BaseModel


class SKUStatusResponse(BaseModel):
    status: str
