from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.homework import HomeworkCreate, HomeworkOut
from app.services.homework_service import create_homework
from app.models.user import User
from app.utils.security import require_role

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