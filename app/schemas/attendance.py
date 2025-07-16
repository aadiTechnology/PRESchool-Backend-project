from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime

class AttendanceMark(BaseModel):
    userId: int
    isPresent: bool

class AttendanceMarkRequest(BaseModel):
    divisionId: int
    date: date
    attendance: List[AttendanceMark]

class AttendanceOut(BaseModel):
    id: int
    userId: int
    divisionId: int
    scanTime: Optional[datetime] = None  # <-- This is correct
    date: date
    status: str
    createdAt: datetime
    name: str

    class Config:
        orm_mode = True