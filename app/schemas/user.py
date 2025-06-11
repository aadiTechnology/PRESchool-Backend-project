from pydantic import BaseModel, validator
from typing import Optional

class UserCreate(BaseModel):
    firstName: str
    lastName: str
    email: str
    phone: str
    password: str
    confirmPassword: str
    role: int
    preschoolId: Optional[int] = 0  # <-- Add this line

    @validator('role')
    def validate_role(cls, v):
        allowed = [0,1, 2, 3] # 'superadmin','admin', 'Teacher', 'Prantes'
        if v not in allowed:
            raise ValueError(f'role must be one of {allowed}')
        return v

class UserOut(BaseModel):
    id: int
    firstName: str
    lastName: str
    email: str
    phone: str
    role: int
    preschoolId: Optional[int] = 0

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    firstName: Optional[str]
    lastName: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    password: Optional[str]
    preschoolId: Optional[int]