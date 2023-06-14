from pydantic import BaseModel


class CargotypeResponse(BaseModel):
    cargotype: int
    # description: str

    class Config:
        orm_mode = True
