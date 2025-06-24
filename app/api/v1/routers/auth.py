from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List

from app.schemas.user import UserCreate, UserOut
from app.db.session import get_db
from app.services.user_service import create_user

router = APIRouter()


@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Force role to 3 (Parent)
    user.role = 3
    try:
        db_user = create_user(db, user)
        return db_user
    except IntegrityError as e:
        db.rollback()
        print("IntegrityError:", e)  # For debugging; use logging in production
        raise HTTPException(status_code=400, detail="Email already registered")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/bulk-register", response_model=List[UserOut])
def bulk_register(
    users: List[UserCreate],
    db: Session = Depends(get_db)
):
    created_users = []
    errors = []
    for idx, user in enumerate(users):
        user.role = 3  # Force role to Parent (or set as needed)
        try:
            db_user = create_user(db, user)
            created_users.append(db_user)
        except IntegrityError as e:
            db.rollback()
            errors.append({"index": idx, "email": user.email, "error": "Email already registered"})
        except Exception as e:
            db.rollback()
            errors.append({"index": idx, "email": user.email, "error": str(e)})
    if errors:
        raise HTTPException(status_code=207, detail={"created": [u.email for u in created_users], "errors": errors})
    return created_users