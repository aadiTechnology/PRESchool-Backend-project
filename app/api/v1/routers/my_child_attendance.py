from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.utils.security import require_role
from app.services.my_child_attendance_service import (
    get_attendance_calendar_data,
    get_daily_attendance_details
)
from app.schemas.my_child_attendance import AttendanceCalendarResponse, DailyAttendanceDetails

router = APIRouter()

@router.get("/my-child/attendance/calendar", response_model=AttendanceCalendarResponse)
def my_child_attendance_calendar(
    userId: int = Query(...),
    classId: int = Query(...),
    divisionId: int = Query(...),
    month: int = Query(..., ge=1, le=12),
    year: int = Query(...),
    db: Session = Depends(get_db),
    current=Depends(require_role([3]))
):
    return get_attendance_calendar_data(db, userId, classId, divisionId, month, year)

@router.get("/my-child/attendance/daily", response_model=DailyAttendanceDetails)
def my_child_attendance_daily(
    userId: int = Query(...),
    classId: int = Query(...),
    divisionId: int = Query(...),
    date: str = Query(...),
    db: Session = Depends(get_db),
    current=Depends(require_role([3]))
):
    return get_daily_attendance_details(db, userId, classId, divisionId, date)