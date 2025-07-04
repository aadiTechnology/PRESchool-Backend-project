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
        preschoolId=user.preschoolId,
        classId=user.classId if user.role in [2, 3] else None,         # <-- Allow for Teacher and Parent
        divisionId=user.divisionId if user.role in [2, 3] else None,   # <-- Allow for Teacher and Parent
        qualification=user.qualification if user.role == 2 else None,
        childName=user.childName if user.role == 3 else None,
        childAge=user.childAge if user.role == 3 else None,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
