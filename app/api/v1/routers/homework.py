from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session, joinedload
from app.db.session import get_db
from app.schemas.homework import HomeworkCreate, HomeworkOut, HomeworkUpdate
from app.models.homework import Homework
from app.models.subject import Subject
from app.models.user import User
from app.utils.security import require_role, get_current_user
from app.services.homework_service import create_homework

router = APIRouter()

@router.post("/assign-homework", response_model=HomeworkOut)
async def assign_homework_json(
    data: HomeworkCreate,
    db: Session = Depends(get_db),
    current=Depends(require_role([2]))
):
    if not data.divisionId or not data.instructions or not data.homeworkDate or not data.subjectId:
        raise HTTPException(status_code=400, detail="Please select division, subject, enter instructions, and select a date.")

    teacher = db.query(User).filter(User.id == current["id"]).first()
    if not teacher:
        raise HTTPException(status_code=403, detail="Teacher not found")
    preschool_id = teacher.preschoolId

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
    db: Session = Depends(get_db),
    current=Depends(get_current_user)
):
    from app.models.subject import Subject

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
            subjectName=subject_name
        ).dict()
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

@router.put("/homeworks/{homework_id}", response_model=HomeworkOut)
def edit_homework(
    homework_id: int,
    data: HomeworkUpdate,
    db: Session = Depends(get_db),
    current=Depends(get_current_user)
):
    homework = db.query(Homework).filter(Homework.id == homework_id).first()
    if not homework:
        raise HTTPException(status_code=404, detail="Homework not found")
    if current["role"] == 2 and homework.teacherId != current["id"]:
        raise HTTPException(status_code=403, detail="Not allowed")

    # Only update provided fields
    update_data = data.dict(exclude_unset=True)
    for field, value in update_data.items():
        if field == "attachments" and value is not None:
            setattr(homework, field, ",".join(value))
        elif value is not None:
            setattr(homework, field, value)

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
    homework_id: int = Path(..., description="The ID of the homework to retrieve"),
    db: Session = Depends(get_db),
    current=Depends(get_current_user)
):
    homework = db.query(Homework).filter(Homework.id == homework_id).first()
    if not homework:
        raise HTTPException(status_code=404, detail="Homework not found")
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