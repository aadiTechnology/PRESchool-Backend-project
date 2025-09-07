from pydantic import BaseModel, model_validator
from typing import Optional

class UserCreate(BaseModel):
    firstName: str
    lastName: str
    email: str
    phone: str
    password: str
    confirmPassword: str
    role: int
    preschoolId: Optional[int] = 0

    # Teacher/Parent-specific fields
    classId: Optional[int] = None
    divisionId: Optional[int] = None
    qualification: Optional[str] = None

    # Parent-specific fields
    fatherName: Optional[str] = None  # <-- Rename from fatherName
    childAge: Optional[int] = None

    @model_validator(mode="after")
    def check_role_fields(self):
        if self.role == 2:
            if not self.classId:
                raise ValueError('classId is required for Teacher registration')
            if not self.divisionId:
                raise ValueError('divisionId is required for Teacher registration')
            if not self.qualification:
                raise ValueError('qualification is required for Teacher registration')
        if self.role == 3:
            if not self.classId:
                raise ValueError('classId is required for Parent registration')
            if not self.divisionId:
                raise ValueError('divisionId is required for Parent registration')
            if not self.fatherName:  
                raise ValueError('fatherName is required for Parent registration')
            if self.childAge is None:
                raise ValueError('childAge is required for Parent registration')
        return self

class UserUpdate(BaseModel):
    firstName: Optional[str]
    lastName: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    password: Optional[str]
    preschoolId: Optional[int]
    classId: Optional[int] = None
    divisionId: Optional[int] = None
    qualification: Optional[str] = None
    fatherName: Optional[str] = None  
    childAge: Optional[int] = None

class UserOut(BaseModel):
    id: int
    firstName: str
    lastName: str
    email: str
    phone: str
    role: int
    preschoolId: Optional[int] = 0
    classId: Optional[int] = None
    divisionId: Optional[int] = None
    qualification: Optional[str] = None
    fatherName: Optional[str] = None  
    childAge: Optional[int] = None

    class Config:
        orm_mode = True

class UserListOut(BaseModel):
    id: int
    firstName: str
    lastName: str
    email: str
    phone: str
    role: int
    preschoolId: Optional[int] = 0
    classId: Optional[int] = None
    divisionId: Optional[int] = None
    className: Optional[str] = None         # <-- Add this
    divisionName: Optional[str] = None      # <-- Add this
    qualification: Optional[str] = None
    fatherName: Optional[str] = None 
    childAge: Optional[int] = None

    class Config:
        orm_mode = True