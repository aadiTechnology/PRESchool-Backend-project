from sqlalchemy.orm import Session
from app.models.syllabus import Syllabus

def create_syllabus(db: Session, month: str, year: int, file_name: str, divisionId: int, teacherId: int, preschoolId: int):
    syllabus = Syllabus(
        month=month,
        year=year,
        file_name=file_name,
        divisionId=divisionId,
        teacherId=teacherId,
        preschoolId=preschoolId
    )
    print(f"Creating syllabus: {syllabus}")
    db.add(syllabus)
    db.commit()
    db.refresh(syllabus)
    return syllabus

def update_syllabus(db: Session, syllabus: Syllabus, file_name: str):
    syllabus.file_name = file_name
    db.commit()
    db.refresh(syllabus)
    return syllabus

def delete_syllabus(db: Session, syllabus: Syllabus):
    db.delete(syllabus)
    db.commit()