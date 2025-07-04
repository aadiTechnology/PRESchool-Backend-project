from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SyllabusOut(BaseModel):
    id: int
    month: str
    year: int
    file_name: str
    divisionId: int
    teacherId: int
    preschoolId: int
    fileUrl: str
    createdAt: datetime

    class Config:
        orm_mode = True