from pydantic import BaseModel, EmailStr, constr
from typing import Optional, Annotated

class PreschoolCreate(BaseModel):
    preschoolName: str
    city: str
    adminFirstName: str
    adminLastName: str
    adminEmail: EmailStr
    initial_password: Optional[str] = None
    adminPhone: Annotated[str, constr(pattern=r'^\+?\d{10,15}$')]

class PreschoolOut(BaseModel):
    id: int
    preschoolName: str
    city: str
    admin_id: int

    class Config:
        orm_mode = True