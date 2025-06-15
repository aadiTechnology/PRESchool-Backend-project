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
    if not data.className or not data.instructions or not data.homeworkDate:
        raise HTTPException(status_code=400, detail="Please select class, enter instructions, and select a date.")

    teacher = db.query(User).filter(User.id == current["id"]).first()
    if not teacher:
        raise HTTPException(status_code=403, detail="Teacher not found")
    preschool_id = teacher.preschoolId

    # File upload code can be added here if you want to support file uploads in the future

    homework = create_homework(db, data, teacher, preschool_id)
    return HomeworkOut(
        id=homework.id,
        className=homework.className,
        homeworkDate=homework.homeworkDate,
        instructions=homework.instructions,
        attachments=homework.attachments.split(",") if homework.attachments else [],
        teacherId=homework.teacherId,
        preschoolId=homework.preschoolId
    )