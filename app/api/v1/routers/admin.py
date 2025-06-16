from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.models.class_ import Class_
from app.models.division import Division
from app.utils.security import get_current_user, require_role
from app.schemas.user import UserOut, UserUpdate, UserCreate, UserListOut
from pydantic import BaseModel
from datetime import datetime, timedelta
from app.utils.security import generate_otp
from app.utils.email_utils import send_otp_email
from app.services.user_service import create_user

router = APIRouter()

class ForgotPasswordRequest(BaseModel):
    email: str

class VerifyOtpRequest(BaseModel):
    email: str
    otp: str

class ResetPasswordRequest(BaseModel):
    email: str
    new_password: str

@router.get("/users", response_model=list[UserListOut])
def list_users(db: Session = Depends(get_db), current=Depends(require_role([0, 1]))):  # 0=superadmin, 1=admin
    users = (
        db.query(
            User,
            Class_.name.label("className"),
            Division.name.label("divisionName")
        )
        .outerjoin(Class_, User.classId == Class_.id)
        .outerjoin(Division, User.divisionId == Division.id)
        .all()
    )
    result = []
    for user, className, divisionName in users:
        user_dict = user.__dict__.copy()
        user_dict["className"] = className
        user_dict["divisionName"] = divisionName
        result.append(UserListOut(**user_dict))
    return result

@router.post("/users", response_model=UserOut)
def add_user(user: UserCreate, db: Session = Depends(get_db), current=Depends(require_role([0, 1]))):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db, user)

@router.put("/users/{user_id}", response_model=UserOut)
def update_user(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db),
    current=Depends(require_role([0, 1]))
):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in user.dict(exclude_unset=True).items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), current=Depends(require_role([0, 1]))):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted"}

@router.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db), current=Depends(require_role([0, 1]))):
    user = db.query(User).filter(User.id == user_id).first()
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

@router.post("/verify-otp")
def verify_otp(request: VerifyOtpRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email.ilike(request.email)).first()
    if not user or not user.otp or not user.otpExpiry:
        raise HTTPException(status_code=400, detail="OTP not found or expired.")
    if user.otp != request.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP.")
    if user.otpExpiry < datetime.utcnow():
        raise HTTPException(status_code=400, detail="OTP expired.")
    # Optionally clear OTP after successful verification
    user.otp = None
    user.otpExpiry = None
    db.commit()
    return {"message": "OTP verified successfully."}

@router.post("/reset-password")
def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email.ilike(request.email)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Optionally, check if OTP was verified before allowing password reset
    from app.utils.security import get_password_hash
    user.hashedPassword = get_password_hash(request.new_password)
    db.commit()
    return {"message": "Password reset successful."}
