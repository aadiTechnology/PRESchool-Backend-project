from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import date

class HomeworkCreate(BaseModel):
    className: str = Field(..., description="Class name")
    homeworkDate: date
    instructions: str
    attachments: Optional[List[str]] = []

class HomeworkOut(BaseModel):
    id: int
    className: str
    homeworkDate: date
    instructions: str
    attachments: List[str]
    teacherId: int
    preschoolId: int

    class Config:
        orm_mode = True