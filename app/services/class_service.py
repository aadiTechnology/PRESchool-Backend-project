from sqlalchemy.orm import Session
from app.models.class_ import Class_

def get_classes_for_preschool(db: Session, preschool_id: int):
    return db.query(Class_).filter(Class_.preschoolId == preschool_id).all()