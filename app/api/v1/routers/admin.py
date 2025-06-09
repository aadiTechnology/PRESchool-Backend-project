from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.utils.security import get_current_user
from app.schemas.user import UserOut, UserUpdate

router = APIRouter()

@router.get("/users")
def list_users(db: Session = Depends(get_db)):
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
