from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import date

class HomeworkCreate(BaseModel):
    divisionId: int = Field(..., description="Division ID")
    subjectId: int = Field(..., description="Subject ID")
    homeworkDate: date
    instructions: str
    attachments: Optional[List[str]] = []

class HomeworkOut(BaseModel):
    id: int
    divisionId: int
    subjectId: int
    homeworkDate: date
    instructions: str
    attachments: List[str]
    teacherId: int
    preschoolId: int
    baseUrl:str
    subjectName: Optional[str] = None

    class Config:
        from_attributes = True

class HomeworkUpdate(BaseModel):
    divisionId: Optional[int] = None
    subjectId: Optional[int] = None
    homeworkDate: Optional[date] = None
    instructions: Optional[str] = None
    attachments: Optional[List[str]] = None