from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db.session import get_db
from app.models.user import User
from app.models.class_ import Class_
from app.utils.security import verify_password
from app.core.jwt import create_access_token

router = APIRouter()

class LoginRequest(BaseModel):
    user_id: str  # can be email or phone
    password: str

@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(
        (User.email == request.user_id) | (User.phone == request.user_id)
    ).first()
    if not user or not verify_password(request.password, user.hashedPassword):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Fetch className if classId is present
    class_name = None
    if user.classId:
        class_obj = db.query(Class_).filter(Class_.id == user.classId).first()
        class_name = class_obj.name if class_obj else None

    access_token = create_access_token(data={
        "sub": user.email,
        "role": user.role,
        "id": user.id,
        "preschoolId": user.preschoolId,
        "classId": user.classId,
        "divisionId": user.divisionId
    })
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "role": user.role,
            "preschoolId": user.preschoolId,
            "classId": user.classId,
            "divisionId": user.divisionId,
            "firstName": user.firstName,
            "lastName": user.lastName,
            "className": class_name   # <-- Add this line
        }
    }
