from fastapi import APIRouter, Depends
from app.utils.security import get_current_user

router = APIRouter()

menus = {
    "admin": ["Dashboard", "Manage Users", "Reports"],
    "teacher": ["Dashboard", "My Classes"],
    "student": ["Dashboard", "Assignments"]
}

@router.get("/menu")
def get_menu(user: dict = Depends(get_current_user)):
    return {"menu": menus.get(user['role'], [])}
