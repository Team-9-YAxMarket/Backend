from pydantic import UUID4, BaseModel


class UserResponse(BaseModel):
    id: UUID4
    username: str

    class Config:
        orm_mode = True
