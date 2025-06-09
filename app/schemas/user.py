from pydantic import BaseModel, validator
from typing import Optional

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    password: str
    confirm_password: str
    role: str

    @validator('role')
    def validate_role(cls, v):
        allowed = ['admin', 'Teacher', 'Prantes']
        if v not in allowed:
            raise ValueError(f'role must be one of {allowed}')
        return v

class UserOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone: str
    role: str  # <-- Add this line

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    password: Optional[str]