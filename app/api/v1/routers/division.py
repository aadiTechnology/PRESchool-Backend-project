from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.division import DivisionOut
from app.services.division_service import get_divisions_for_class
from app.utils.security import get_current_user

router = APIRouter()

@router.get("/divisions", response_model=list[DivisionOut])
def list_divisions(classId: int, db: Session = Depends(get_db), current=Depends(get_current_user)):
    preschool_id = current["preschoolId"]
    return get_divisions_for_class(db, preschool_id, classId)