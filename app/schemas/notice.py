from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime

class NoticeBase(BaseModel):
    title: str = Field(..., example="School Trip Announcement")
    content: str = Field(..., example="We are excited to announce...")
    classId: Optional[int] = Field(None, description="Target class ID, null for all classes")
    date: date
    attachments: Optional[List[str]] = []
    divisionId: Optional[int]  # New field

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
    baseUrl: str  # <-- Add this line

    class Config:
        orm_mode = True