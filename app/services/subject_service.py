from sqlalchemy.orm import Session
from app.models.subject import Subject

def get_subjects_for_class(db: Session, preschool_id: int, divisionId: int):
    return db.query(Subject).filter(
        Subject.preschoolId == preschool_id,
        Subject.divisionId == divisionId
    ).all()