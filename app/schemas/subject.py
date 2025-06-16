from pydantic import BaseModel

class SubjectOut(BaseModel):
    id: int
    name: str
    classId: int        # <-- ADD this line
    preschoolId: int

    class Config:
        orm_mode = True