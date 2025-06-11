from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.preschool import PreschoolCreate
from app.services.preschool_service import create_preschool_with_admin
from app.db.session import get_db

router = APIRouter()

@router.post("/register-preschool")
def register_preschool(
    data: PreschoolCreate,
    db: Session = Depends(get_db)
):
    try:
        preschool, admin_user, password = create_preschool_with_admin(db, data)
        return {
            "message": "Preschool and admin successfully created.",
            "preschoolId": preschool.id,
            "adminId": admin_user.id,
            "generatedPassword": password if not data.initial_password else None
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))