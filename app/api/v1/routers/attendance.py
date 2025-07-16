from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.attendance import AttendanceMarkRequest, AttendanceOut
from app.services.attendance_service import (
    mark_attendance_teacher,
    get_students_for_division,
    get_attendance_for_division_date
)
from app.utils.security import require_role, get_current_user
from datetime import date

router = APIRouter()

@router.get("/attendance/students", response_model=list[dict])
def list_students_for_division(
    divisionId: int = Query(...),
    db: Session = Depends(get_db),
    current=Depends(require_role([2]))  # Teacher only
):
    return get_students_for_division(db, divisionId)

@router.get("/attendance", response_model=list[AttendanceOut])
def get_attendance_for_division(
    divisionId: int = Query(...),
    date_: date = Query(..., alias="date"),
    db: Session = Depends(get_db),
    current=Depends(require_role([2]))
):
    records = get_attendance_for_division_date(db, divisionId, date_)
    if not records:
        raise HTTPException(status_code=404, detail="No Attendance Found For This Date.")
    return [AttendanceOut(**r) for r in records]

@router.post("/attendance/mark", response_model=dict)
def mark_attendance(
    data: AttendanceMarkRequest,
    db: Session = Depends(get_db),
    current=Depends(require_role([2]))
):
    # Validate date (no future, no holiday logic here)
    from datetime import date as dt_date
    if data.date > dt_date.today():
        raise HTTPException(status_code=400, detail="Cannot mark attendance for future date.")
    # TODO: Add holiday check if needed
    if not data.attendance or not any(a.isPresent for a in data.attendance):
        raise HTTPException(status_code=400, detail="At least one student must be marked present.")
    mark_attendance_teacher(db, data.divisionId, data.date, data.attendance)
    return {"message": "Attendance saved successfully."}