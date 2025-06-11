from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.utils.security import get_password_hash

def create_user(db: Session, user: UserCreate):
    db_user = User(
        firstName=user.firstName,
        lastName=user.lastName,
        email=user.email,
        phone=user.phone,
        hashedPassword=get_password_hash(user.password),
        role=user.role,
        preschoolId=user.preschoolId  # <-- Add this line
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
