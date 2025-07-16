from sqlalchemy.orm import Session
from app.models.attendance import Attendance
from app.models.user import User
from datetime import datetime, date  # <-- Add this import

def mark_attendance_teacher(db: Session, division_id: int, date_: date, attendance_list: list):
    for item in attendance_list:
        user = db.query(User).filter(User.id == item.userId, User.divisionId == division_id).first()
        if not user:
            continue
        att = db.query(Attendance).filter(
            Attendance.userId == user.id,
            Attendance.divisionId == division_id,
            Attendance.date == date_
        ).first()
        status = "Present" if item.isPresent else "Absent"
        scan_time = datetime.now() if item.isPresent else None
        if att:
            att.status = status
            att.scanTime = scan_time
            db.commit()
            db.refresh(att)
        else:
            att = Attendance(
                userId=user.id,
                divisionId=division_id,
                scanTime=scan_time,
                date=date_,
                status=status
            )
            db.add(att)
            db.commit()
            db.refresh(att)
    return True

def get_students_for_division(db: Session, division_id: int):
    students = db.query(User).filter(User.divisionId == division_id, User.role == 3).all()
    return [{"userId": s.id, "name": f"{s.firstName} {s.lastName}"} for s in students]

def get_attendance_for_division_date(db: Session, division_id: int, date_: date):
    from app.models.user import User
    students = db.query(User).filter(User.divisionId == division_id, User.role == 3).all()
    attendance_map = {
        a.userId: a for a in db.query(Attendance).filter(
            Attendance.divisionId == division_id,
            Attendance.date == date_
        ).all()
    }
    result = []
    for idx, s in enumerate(students, start=1):
        att = attendance_map.get(s.id)
        result.append({
            "id": att.id if att else idx,  # <-- Use idx or 0 instead of None
            "userId": s.id,
            "divisionId": division_id,
            "scanTime": att.scanTime if att and att.scanTime else None,
            "date": date_,
            "status": att.status if att else "Absent",
            "createdAt": att.createdAt if att else datetime.now(),
            "name": f"{s.firstName} {s.lastName}"
        })
    return result