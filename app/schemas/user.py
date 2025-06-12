from pydantic import BaseModel, field_validator, model_validator
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

    # Teacher-specific fields
    className: Optional[str] = None
    qualification: Optional[str] = None

    # Parent-specific fields
    childName: Optional[str] = None
    childAge: Optional[int] = None
    childClass: Optional[str] = None

    @model_validator(mode="after")
    def check_role_fields(self):
        if self.role == 2:
            if not self.className:
                raise ValueError('className is required for Teacher registration')
            if not self.qualification:
                raise ValueError('qualification is required for Teacher registration')
        if self.role == 3:
            if not self.childName:
                raise ValueError('childName is required for Parent registration')
            if self.childAge is None:
                raise ValueError('childAge is required for Parent registration')
            if not self.childClass:
                raise ValueError('childClass is required for Parent registration')
        return self

class UserOut(BaseModel):
    id: int
    firstName: str
    lastName: str
    email: str
    phone: str
    role: int
    preschoolId: Optional[int] = 0
    className: Optional[str] = None
    qualification: Optional[str] = None
    childName: Optional[str] = None
    childAge: Optional[int] = None
    childClass: Optional[str] = None

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    firstName: Optional[str]
    lastName: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    password: Optional[str]
    preschoolId: Optional[int]
    className: Optional[str] = None
    qualification: Optional[str] = None
    childName: Optional[str] = None
    childAge: Optional[int] = None
    childClass: Optional[str] = None