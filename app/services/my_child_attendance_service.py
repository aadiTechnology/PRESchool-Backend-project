from sqlalchemy.orm import Session
from app.models.user import User
from app.models.class_ import Class_
from app.models.attendance import Attendance
from datetime import datetime, date, timedelta
from fastapi import HTTPException

def get_attendance_calendar_data(db: Session, user_id: int, class_id: int, division_id: int, month: int, year: int):
    # Fetch the child directly by userId, classId, and divisionId
    child = db.query(User).filter(
        User.id == user_id,
        User.classId == class_id,
        User.divisionId == division_id
    ).first()
    if not child:
        raise HTTPException(status_code=404, detail="Child not found")
    class_ = db.query(Class_).filter(Class_.id == class_id).first()
    if not class_:
        raise HTTPException(status_code=404, detail="Class not found")

    start_date = date(year, month, 1)
    if month == 12:
        end_date = date(year + 1, 1, 1)
    else:
        end_date = date(year, month + 1, 1)
    records = db.query(Attendance).filter(
        Attendance.userId == child.id,
        Attendance.divisionId == division_id,
        Attendance.date >= start_date,
        Attendance.date < end_date
    ).all()
    attendance_map = {a.date: a.status for a in records}

    days_in_month = (end_date - start_date).days
    calendar = []
    present_days = absent_days = 0
    for i in range(days_in_month):
        d = start_date + timedelta(days=i)
        status = attendance_map.get(d, "NotMarked")
        if status == "Present":
            present_days += 1
        elif status == "Absent":
            absent_days += 1
        calendar.append({
            "date": d.isoformat(),
            "status": status
        })
    total_days = present_days + absent_days
    attendance_rate = int((present_days / total_days) * 100) if total_days else 0

    return {
        "childName": f"{child.firstName} {child.lastName}",
        "className": class_.name,
        "presentDays": present_days,
        "absentDays": absent_days,
        "attendanceRate": attendance_rate,
        "calendar": calendar
    }

def get_daily_attendance_details(db: Session, user_id: int, class_id: int, division_id: int, date_str: str):
    child = db.query(User).filter(
        User.id == user_id,
        User.classId == class_id,
        User.divisionId == division_id
    ).first()
    if not child:
        raise HTTPException(status_code=404, detail="Child not found")
    att = db.query(Attendance).filter(
        Attendance.userId == child.id,
        Attendance.divisionId == division_id,
        Attendance.date == date.fromisoformat(date_str)
    ).first()
    if not att:
        return {
            "date": date_str,
            "status": "NotMarked",
            "message": "Attendance Not Marked"
        }
    if att.status == "Absent":
        return {
            "date": date_str,
            "status": "Absent"
        }
    scan_time = att.scanTime.strftime("%I:%M %p") if att.scanTime else None
    teacher_obj = db.query(User).filter(User.divisionId == division_id, User.role == 2).first()
    teacher_name = f"{teacher_obj.firstName} {teacher_obj.lastName}" if teacher_obj else None
    return {
        "date": date_str,
        "status": att.status,
        "scanTime": scan_time,
        "teacherName": teacher_name
    }