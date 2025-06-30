from fastapi import APIRouter, Depends, HTTPException, Path, File, UploadFile, Form, Request
from sqlalchemy.orm import Session, joinedload
from app.db.session import get_db
from app.schemas.homework import HomeworkCreate, HomeworkOut, HomeworkUpdate
from app.models.homework import Homework
from app.models.subject import Subject
from app.models.user import User
from app.utils.security import require_role, get_current_user
from app.services.homework_service import create_homework
from app.core.config import settings
import os
from datetime import datetime

router = APIRouter()

@router.post("/assign-homework", response_model=HomeworkOut)
async def assign_homework_json(
    divisionId: int = Form(...),
    subjectId: int = Form(...),
    homeworkDate: str = Form(...),
    instructions: str = Form(...),
    attachments: list[UploadFile] = File([]),
    db: Session = Depends(get_db),
    current=Depends(require_role([2]))
):
    # Validate required fields
    if not divisionId or not instructions or not homeworkDate or not subjectId:
        raise HTTPException(status_code=400, detail="Please select division, subject, enter instructions, and select a date.")

    teacher = db.query(User).filter(User.id == current["id"]).first()
    if not teacher:
        raise HTTPException(status_code=403, detail="Teacher not found")
    preschool_id = teacher.preschoolId

    # Save files
    tenant_id = str(current["preschoolId"])  # Get tenant id from the current user/session
    upload_dir = os.path.join(settings.HOMEWORK_UPLOAD_DIR, tenant_id)
    os.makedirs(upload_dir, exist_ok=True)
    saved_filenames = []
    for file in attachments:
        filename = f"{int(datetime.now().timestamp())}_{file.filename}"
        file_path = os.path.join(upload_dir, filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())
        saved_filenames.append(filename)

    # Prepare data for service
    class DummyData:
        pass
    data = DummyData()
    data.divisionId = divisionId
    data.subjectId = subjectId
    data.homeworkDate = homeworkDate
    data.instructions = instructions
    data.attachments = saved_filenames

    homework = create_homework(db, data, teacher, preschool_id)
    return HomeworkOut(
        id=homework.id,
        divisionId=homework.divisionId,
        subjectId=homework.subjectId,
        homeworkDate=homework.homeworkDate,
        instructions=homework.instructions,
        attachments=homework.attachments.split(",") if homework.attachments else [],
        teacherId=homework.teacherId,
        preschoolId=homework.preschoolId
    )

@router.get("/homeworks", response_model=list[HomeworkOut])
def list_homeworks(
    divisionId: int,
    request: Request,  # <-- Add this
    db: Session = Depends(get_db),
    current=Depends(get_current_user)
):
    query = db.query(
        Homework,
        Subject.name.label("subjectName")
    ).join(Subject, Homework.subjectId == Subject.id)

    if current["role"] == 2:  # Teacher
        query = query.filter(Homework.teacherId == current["id"], Homework.divisionId == divisionId)
    elif current["role"] == 3:  # Parent
        query = query.filter(Homework.divisionId == divisionId)
    else:
        raise HTTPException(status_code=403, detail="Access denied")

    # Order by homeworkDate descending
    query = query.order_by(Homework.homeworkDate.desc())

    results = query.all()
    output = []
    tenant_id = str(current["preschoolId"])
    base_url = f"{request.base_url}{settings.HOMEWORK_UPLOAD_DIR}/{tenant_id}/"
    for hw, subject_name in results:
        attachments_list = hw.attachments.split(",") if hw.attachments else []
        hw_dict = HomeworkOut(
            id=hw.id,
            divisionId=hw.divisionId,
            subjectId=hw.subjectId,
            homeworkDate=hw.homeworkDate,
            instructions=hw.instructions,
            attachments=attachments_list,
            teacherId=hw.teacherId,
            preschoolId=hw.preschoolId,
            subjectName=subject_name,
            baseUrl=base_url
        ).dict()
        hw_dict["baseUrl"] = base_url  # <-- Add baseUrl to each homework
        output.append(hw_dict)
    return output

@router.delete("/homeworks/{homework_id}")
def delete_homework(
    homework_id: int,
    db: Session = Depends(get_db),
    current=Depends(get_current_user)
):
    homework = db.query(Homework).filter(Homework.id == homework_id).first()
    if not homework:
        raise HTTPException(status_code=404, detail="Homework not found")
    # Only teacher who created or admin can delete
    if current["role"] == 2 and homework.teacherId != current["id"]:
        raise HTTPException(status_code=403, detail="Not allowed")
    db.delete(homework)
    db.commit()
    return {"message": "Homework deleted"}

from fastapi import Form, UploadFile, File

@router.put("/homeworks/{homework_id}", response_model=HomeworkOut)
async def edit_homework(
    homework_id: int,
    divisionId: int = Form(...),
    subjectId: int = Form(...),
    homeworkDate: str = Form(...),
    instructions: str = Form(...),
    attachments: list[UploadFile] = File([]),
    db: Session = Depends(get_db),
    current=Depends(get_current_user)
):
    homework = db.query(Homework).filter(Homework.id == homework_id).first()
    if not homework:
        raise HTTPException(status_code=404, detail="Homework not found")
    if current["role"] == 2 and homework.teacherId != current["id"]:
        raise HTTPException(status_code=403, detail="Not allowed")

    # Save new files
    tenant_id = str(current["preschoolId"])  # Get tenant id from the current user/session
    upload_dir = os.path.join(settings.HOMEWORK_UPLOAD_DIR, tenant_id)
    os.makedirs(upload_dir, exist_ok=True)
    saved_filenames = []
    for file in attachments:
        filename = f"{int(datetime.now().timestamp())}_{file.filename}"
        file_path = os.path.join(upload_dir, filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())
        saved_filenames.append(filename)

    # Merge with existing attachments
    existing_files = homework.attachments.split(",") if homework.attachments else []
    all_files = existing_files + saved_filenames

    # Update fields
    homework.divisionId = divisionId
    homework.subjectId = subjectId
    homework.homeworkDate = homeworkDate
    homework.instructions = instructions
    homework.attachments = ",".join(all_files)

    db.commit()
    db.refresh(homework)
    subject = db.query(Subject).filter(Subject.id == homework.subjectId).first()
    return HomeworkOut(
        id=homework.id,
        divisionId=homework.divisionId,
        subjectId=homework.subjectId,
        homeworkDate=homework.homeworkDate,
        instructions=homework.instructions,
        attachments=homework.attachments.split(",") if homework.attachments else [],
        teacherId=homework.teacherId,
        preschoolId=homework.preschoolId,
        subjectName=subject.name if subject else None
    )

@router.get("/homeworks/{homework_id}", response_model=HomeworkOut)
def get_homework(
    request: Request,
    homework_id: int = Path(..., description="The ID of the homework to retrieve"),
    db: Session = Depends(get_db),
    current=Depends(get_current_user)
):
    homework = db.query(Homework).filter(Homework.id == homework_id).first()
    if not homework:
        raise HTTPException(status_code=404, detail="Homework not found")
    subject = db.query(Subject).filter(Subject.id == homework.subjectId).first()
    tenant_id = str(current["preschoolId"])
    base_url = f"{request.base_url}{settings.HOMEWORK_UPLOAD_DIR}/{tenant_id}/"
    return HomeworkOut(
        id=homework.id,
        divisionId=homework.divisionId,
        subjectId=homework.subjectId,
        homeworkDate=homework.homeworkDate,
        instructions=homework.instructions,
        attachments=homework.attachments.split(",") if homework.attachments else [],
        teacherId=homework.teacherId,
        preschoolId=homework.preschoolId,
        subjectName=subject.name if subject else None,
        baseUrl=base_url
    )