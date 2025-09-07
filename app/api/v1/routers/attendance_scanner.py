from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.db.session import get_db

from app.models.attendance import Attendance
from app.schemas.attendance_schemas import AttendanceScanRequest, AttendanceScanResponse, AttendanceSaveRequest
from datetime import datetime, date

from app.models.user import User
from app.models.class_ import Class_
from app.models.division import Division

import os
import json
from sqlalchemy import func

print("DB URL:", os.getenv("SQLALCHEMY_DATABASE_URL"))
router = APIRouter()


@router.post("/attendance/scan", response_model=AttendanceScanResponse)
def scan_attendance(
    data: AttendanceScanRequest,
    db: Session = Depends(get_db)
):
    qr_data = data.qr_code
    user_id = qr_data.id
    first_name = qr_data.firstName
    last_name = qr_data.lastName
    role = str(qr_data.role)

    user = None
    if user_id and last_name and role:
        query = db.query(User).filter(User.id == user_id)
        if role == "1" or role == "3":  # Teacher
            if first_name:
                query = query.filter(func.lower(User.firstName) == first_name.lower())
        query = query.filter(func.lower(User.lastName) == last_name.lower())
        query = query.filter(User.role == role)
        user = query.first()
    else:
        if isinstance(data.qr_code, str) and data.qr_code.isdigit():
            user = db.query(User).filter(User.id == int(data.qr_code)).first()
        else:
            user = db.query(User).filter(User.email == data.qr_code).first()

    if not user:
        return {
            "status": "failed",
            "user": None,
            "message": "Invalid card or user not found",
            "stats": {
                "totalScansToday": 0,
                "teachersPresent": 0,
                "studentsPresent": 0
            }
        }

    preschool_id = user.preschoolId
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

    today = date.today()
    existing_attendance = db.query(Attendance).filter(
        Attendance.userId == user.id,
        Attendance.date == today,
        Attendance.status == "Present"
    ).first()

    students_present = db.query(Attendance).join(
        User, Attendance.userId == User.id
    ).filter(
        Attendance.date == today,
        Attendance.status == "Present",
        User.role == "3"
    ).count()
    teachers_present = db.query(Attendance).join(
        User, Attendance.userId == User.id
    ).filter(
        Attendance.date == today,
        Attendance.status == "Present",
        User.role == "2"
    ).count()
    total_scans = db.query(Attendance).filter(
        Attendance.date == today,
        Attendance.status == "Present"
    ).count()
    display_name = f"{user.firstName} {user.lastName}"
    if str(user.role) == "2":
        user_role = "Teacher"
    elif str(user.role) == "3":
        user_role = "Student"
    else:
        user_role = "Admin"

    # If already marked, return info with last scan time and custom message
    if existing_attendance:
        scan_time = existing_attendance.scanTime.strftime("%H:%M:%S") if existing_attendance.scanTime else ""
        return {
            "status": "failed",
            "user": {
                "id": user.id,
                "fullName": display_name,
                "role": user_role,
                "className": class_name,
                "divisionName": division_name,
                "divisionId": user.divisionId,
                "email": user.email,
                "scanTime": scan_time,
                "date": today.strftime("%Y-%m-%d")
            },
            "message": f"Attendance already marked for {display_name} on {today.strftime('%Y-%m-%d')}",
            "stats": {
                "totalScansToday": total_scans,
                "teachersPresent": teachers_present,
                "studentsPresent": students_present
            }
        }

    # Directly save attendance if not already marked
    now = datetime.now()
    new_att = Attendance(
        userId=user.id,
        divisionId=user.divisionId,
        scanTime=now,
        date=today,
        status="Present",
    )
    db.add(new_att)
    db.commit()
    db.refresh(new_att)

    # Recalculate stats after saving attendance
    students_present = db.query(Attendance).join(
        User, Attendance.userId == User.id
    ).filter(
        Attendance.date == today,
        Attendance.status == "Present",
        User.role == "3"
    ).count()
    teachers_present = db.query(Attendance).join(
        User, Attendance.userId == User.id
    ).filter(
        Attendance.date == today,
        Attendance.status == "Present",
        User.role == "2"
    ).count()
    total_scans = db.query(Attendance).filter(
        Attendance.date == today,
        Attendance.status == "Present"
    ).count()

    return {
        "status": "success",
        "user": {
            "id": user.id,
            "fullName": display_name,
            "role": user_role,
            "className": class_name,
            "divisionName": division_name,
            "divisionId": user.divisionId,
            "email": user.email,
            "scanTime": now.strftime("%H:%M:%S"),
            "date": today.strftime("%Y-%m-%d")
        },
        "message": f"Attendance marked successfully for {display_name}",
        "stats": {
            "totalScansToday": total_scans,
            "teachersPresent": teachers_present,
            "studentsPresent": students_present
        }
    }


@router.post("/attendance/save")
def save_attendance(
    data: AttendanceSaveRequest,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == data.userId).first()
    if not user:
        return {
            "status": "failed",
            "message": "User not found"
        }

    preschool_id = user.preschoolId
    division_id = user.divisionId

    att = db.query(Attendance ).filter(
        Attendance .userId == data.userId,
        Attendance .date == data.date_,
       
        Attendance .status == "Present"
    ).first()
    if att:
        return {
            "status": "failed",
            "message": f"Attendance already marked for this user on {data.date_}"
        }

    new_att = Attendance (
        userId=data.userId,
        divisionId=division_id,
        scanTime=datetime.now(),
        date=data.date_,
        status="Present",
        preschoolId=preschool_id
    )
    db.add(new_att)
    db.commit()

    display_name = f"{user.firstName} {user.lastName}"

    return {
        "status": "success",
        "message": f"Attendance marked successfully for {display_name}"
    }
@router.get("/attendance/stats")
def get_attendance_stats(
    db: Session = Depends(get_db),
    date_: date = Query(..., description="Date for stats (YYYY-MM-DD)"),
    
):
    print("DEBUG: date_ param received:", date_)
    students_present = db.query(Attendance ).join(
        User, Attendance .userId == User.id
    ).filter(
        Attendance .date == date_,
        Attendance .status == "Present",
        User.role == "3"
    ).count()

    teachers_present = db.query(Attendance ).join(
        User, Attendance .userId == User.id
    ).filter(
        Attendance .date == date_,
        Attendance .status == "Present",
        User.role == "2"  # <-- use "2" for teacher role
    ).count()

    total_scans = db.query(Attendance ).filter(
        Attendance .date == date_,
        Attendance .status == "Present"
    ).count()

    print(f"Attendance records for {date_} ",
          db.query(Attendance ).filter(
              Attendance .date == date_,
              
          ).all())

    return {
        "totalScansToday": total_scans,
        "teachersPresent": teachers_present,
        "studentsPresent": students_present
    }