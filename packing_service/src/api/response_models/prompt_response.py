from pydantic import UUID4, BaseModel


class PromptResponse(BaseModel):
    id: UUID4
    prompt: str

    class Config:
        orm_mode = True
