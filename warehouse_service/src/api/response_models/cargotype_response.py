from pydantic import BaseModel


class CargotypeResponse(BaseModel):
    cargotype: int

    class Config:
        orm_mode = True
