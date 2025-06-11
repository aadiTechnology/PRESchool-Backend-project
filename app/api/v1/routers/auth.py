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
        hashedPassword = get_password_hash(user.password)
        db_user = User(
            firstName=user.firstName,
            lastName=user.lastName,
            email=user.email,
            phone=user.phone,
            hashedPassword=hashedPassword,
            role=user.role, 
            preschoolId=user.preschoolId
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError as e:
        db.rollback()
        print("IntegrityError:", e)  # For debugging; use logging in production
        raise HTTPException(status_code=400, detail="Email already registered")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))