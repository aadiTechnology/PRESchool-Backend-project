from sqlalchemy.orm import Session
from app.models.homework import Homework
from app.models.user import User

def create_homework(db: Session, data, teacher: User, preschool_id: int):
    homework = Homework(
        className=data.className,
        homeworkDate=data.homeworkDate,
        instructions=data.instructions,
        attachments=",".join(data.attachments),
        teacherId=teacher.id,
        preschoolId=preschool_id
    )
    db.add(homework)
    db.commit()
    db.refresh(homework)
    return homework