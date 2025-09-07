from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime
from pydantic import BaseModel
from typing import Optional
from pydantic import BaseModel
from datetime import date

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
    scanTime: Optional[str] = None  # <-- Change to str
    date: date
    status: str
    createdAt: datetime
    name: str

    class Config:
        orm_mode = True


class QRCodeData(BaseModel):
    id: int
    firstName: Optional[str] = None
    lastName: str
    role: int

class AttendanceScanRequest(BaseModel):
    qr_code: QRCodeData

class AttendanceUser(BaseModel):
    id: int
    fullName: str
    role: str
    className: Optional[str]
    divisionName: Optional[str]
    divisionId: Optional[int]   # <-- Add this line
    email: Optional[str]
    scanTime: Optional[str]
    date: Optional[str]

class AttendanceStats(BaseModel):
    totalScansToday: int
    teachersPresent: int
    studentsPresent: int

class AttendanceScanResponse(BaseModel):
    status: str
    user: Optional[AttendanceUser]
    message: str
    stats: AttendanceStats



class AttendanceSaveRequest(BaseModel):
    userId: int
    date_: date
    status: str = "Present"