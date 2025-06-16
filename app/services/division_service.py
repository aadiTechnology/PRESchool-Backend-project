from sqlalchemy.orm import Session
from app.models.division import Division

def get_divisions_for_class(db: Session, preschool_id: int, class_id: int):
    print(f"Fetching divisions for preschool_id: {preschool_id}, class_id: {class_id}")
    return db.query(Division).filter(
        Division.preschoolId == preschool_id,
        Division.classId == class_id
    ).all()