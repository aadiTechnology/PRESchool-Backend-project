from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.schemas.user import UserCreate, UserOut
from app.db.session import get_db
from app.utils.security import get_password_hash
from app.models.user import User

router = APIRouter()


@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        hashed_password = get_password_hash(user.password)
        db_user = User(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            phone=user.phone,
            hashed_password=hashed_password,
            role=user.role,  # <-- Add this line
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))