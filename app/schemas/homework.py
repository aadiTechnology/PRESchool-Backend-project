from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import date

class HomeworkCreate(BaseModel):
    divisionId: int = Field(..., description="Division ID")  # <-- NEW
    subjectId: int = Field(..., description="Subject ID")
    homeworkDate: date
    instructions: str
    attachments: Optional[List[str]] = []

class HomeworkOut(BaseModel):
    id: int
    divisionId: int  # <-- NEW
    subjectId: int
    homeworkDate: date
    instructions: str
    attachments: List[str]
    teacherId: int
    preschoolId: int

    class Config:
        orm_mode = True