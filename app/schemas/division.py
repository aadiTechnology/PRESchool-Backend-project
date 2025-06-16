from pydantic import BaseModel

class DivisionOut(BaseModel):
    id: int
    name: str
    classId: int
    preschoolId: int

    class Config:
        orm_mode = True