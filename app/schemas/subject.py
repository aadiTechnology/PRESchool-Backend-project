from pydantic import BaseModel

class SubjectOut(BaseModel):
    id: int
    name: str
    className: str
    preschoolId: int

    class Config:
        orm_mode = True