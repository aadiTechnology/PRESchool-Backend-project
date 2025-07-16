from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime

class NoticeBase(BaseModel):
    title: str
    content: str
    classId: Optional[int]
    divisionId: Optional[int]  # Make divisionId optional
    date: date
    attachments: Optional[List[str]] = []

class NoticeCreate(NoticeBase):
    pass

class NoticeUpdate(NoticeBase):
    pass

class NoticeOut(NoticeBase):
    id: int
    preschoolId: int
    createdBy: int
    className: Optional[str] = None
    createdAt: datetime
    updatedAt: datetime
    baseUrl: str

    class Config:
        orm_mode = True