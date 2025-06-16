from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.subject import SubjectOut
from app.services.subject_service import get_subjects_for_class
from app.utils.security import get_current_user

router = APIRouter()

@router.get("/subjects", response_model=list[SubjectOut])
def list_subjects(divisionId: int, db: Session = Depends(get_db), current=Depends(get_current_user)):
    preschool_id = current["preschoolId"]
    subjects = get_subjects_for_class(db, preschool_id, divisionId)
    return subjects