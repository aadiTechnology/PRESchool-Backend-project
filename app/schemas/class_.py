from pydantic import BaseModel

class ClassOut(BaseModel):
    id: int
    name: str
    preschoolId: int

    class Config:
        orm_mode = True