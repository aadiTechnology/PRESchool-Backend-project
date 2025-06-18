from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.class_ import ClassOut
from app.services.class_service import get_classes_for_preschool

router = APIRouter()

@router.get("/classes", response_model=list[ClassOut])
def list_classes(preschoolId: int, db: Session = Depends(get_db)):
    return get_classes_for_preschool(db, preschoolId)

@router.get("/public-classes", response_model=list[ClassOut])
def public_list_classes(preschoolId: int, db: Session = Depends(get_db)):
    """
    Public endpoint: List classes for a preschool (no authentication required)
    """
    return get_classes_for_preschool(db, preschoolId)