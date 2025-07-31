from pydantic import BaseModel
from typing import List, Optional

class AttendanceCalendarDay(BaseModel):
    date: str
    status: str  # "Present", "Absent", "NotMarked"

class AttendanceCalendarResponse(BaseModel):
    childName: str
    className: str
    presentDays: int
    absentDays: int
    attendanceRate: int
    calendar: List[AttendanceCalendarDay]

class DailyAttendanceDetails(BaseModel):
    date: str
    status: str
    scanTime: Optional[str] = None
    teacherName: Optional[str] = None
    message: Optional[str] = None