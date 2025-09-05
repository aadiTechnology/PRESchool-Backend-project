from sqlalchemy.orm import Session
from app.models.attendance import Attendance
from app.models.user import User
from datetime import datetime, date
from sqlalchemy.orm import Session
from datetime import datetime, date


from app.models.class_ import Class_
from app.models.division import Division


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
        # Format scanTime if present
        scan_time_str = (
            att.scanTime.strftime("%d-%m-%Y %I:%M %p") if att and att.scanTime else None
        )
        result.append({
            "id": att.id if att else idx,
            "userId": s.id,
            "divisionId": division_id,
            "scanTime": scan_time_str,  # <-- Formatted string
            "date": date_,
            "status": att.status if att else "Absent",
            "createdAt": att.createdAt if att else datetime.now(),
            "name": f"{s.firstName} {s.lastName}"
        })
    return result


def scan_and_mark_attendance(db, qr_code: str, preschool_id: int):
    # 1. Find user by QR code (id or email)
    if qr_code.isdigit():
        user = db.query(User).filter(
            User.id == int(qr_code),
            User.preschoolId == preschool_id
        ).first()
    else:
        user = db.query(User).filter(
            User.email == qr_code,
            User.preschoolId == preschool_id
        ).first()
    if not user:
        return None, "Invalid card or user not found"

    # 2. Get class and division info
    class_name = None
    division_name = None
    if user.classId:
        class_obj = db.query(Class_).filter(Class_.id == user.classId).first()
        if class_obj:
            class_name = class_obj.name
    if user.divisionId:
        division_obj = db.query(Division).filter(Division.id == user.divisionId).first()
        if division_obj:
            division_name = division_obj.name

    # 3. Check if already marked today
    today = date.today()
    now = datetime.now()
    att = db.query(Attendance).filter(
        Attendance.userId == user.id,
        Attendance.date == today,
        Attendance.preschoolId == preschool_id,
        Attendance.status == "Present"
    ).first()
    if att:
        return {
            "status": "failed",
            "user": {
                "id": user.id,
                "fullName": f"{user.firstName} {user.lastName}",
                "role": "Teacher" if user.role == "2" else "Student" if user.role == "3" else "Admin",
                "className": class_name,
                "divisionName": division_name,
                "scanTime": att.scanTime.strftime("%H:%M:%S") if att.scanTime else "",
                "date": today.strftime("%Y-%m-%d")
            },
            "message": f"Attendance already marked for {user.firstName} {user.lastName} on {today.strftime('%Y-%m-%d')}",
            "stats": {
                "totalScansToday": 0,
                "teachersPresent": 0,
                "studentsPresent": 0
            }
        }, None

    # 4. Mark attendance
    new_att = Attendance(
        userId=user.id,
        divisionId=user.divisionId,
        scanTime=now,
        date=today,
        status="Present",
        preschoolId=preschool_id
    )
    db.add(new_att)
    db.commit()
    db.refresh(new_att)

    return {
        "status": "success",
        "user": {
            "id": user.id,
            "fullName": f"{user.firstName} {user.lastName}",
            "role": "Teacher" if user.role == "2" else "Student" if user.role == "3" else "Admin",
            "className": class_name,
            "divisionName": division_name,
            "scanTime": now.strftime("%H:%M:%S"),
            "date": today.strftime("%Y-%m-%d")
        },
        "message": f"Attendance marked successfully for {user.firstName} {user.lastName}",
        "stats": {
            "totalScansToday": 0,
            "teachersPresent": 0,
            "studentsPresent": 0
        }
    }, None