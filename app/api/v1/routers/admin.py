from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.utils.security import get_current_user, require_role
from app.schemas.user import UserOut, UserUpdate
from pydantic import BaseModel
from datetime import datetime, timedelta
from app.utils.security import generate_otp
from app.utils.email_utils import send_otp_email

router = APIRouter()

class ForgotPasswordRequest(BaseModel):
    email: str

@router.get("/users")
def list_users(db: Session = Depends(get_db), current=Depends(require_role(["admin", "superadmin"]))):
    return db.query(User).all()

@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), current=Depends(get_current_user)):
    if current['role'] != 'admin':
        raise HTTPException(status_code=403, detail="Access denied")
    user = db.query(User).filter(User.id == user_id).first()
    print(user)  # Check what is printed in the logs
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted"}

@router.put("/users/{user_id}")
def update_user(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db),
    current=Depends(get_current_user)
):
    if current['role'] != 'admin':
        raise HTTPException(status_code=403, detail="Access denied")
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in user.dict(exclude_unset=True).items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return {"message": "User updated"}

@router.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db), current=Depends(get_current_user)):
    if current['role'] != 'admin':
        raise HTTPException(status_code=403, detail="Access denied")
    user = db.query(User).filter(User.id == user_id).first()
    print(user)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/forgot-password")
def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email.ilike(request.email)).first()
    if not user:
        raise HTTPException(status_code=404, detail="Email not found. Try again.")
    otp = generate_otp()
    print("Generated OTP:", otp)
    user.otp = otp
    user.otpExpiry = datetime.utcnow() + timedelta(minutes=10)
    print("User OTP before commit:", user.otp)
    db.commit()
    send_otp_email(user.email, otp)
    return {"message": "OTP sent to your email address."}
