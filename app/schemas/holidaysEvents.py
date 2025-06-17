from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class HolidaysEventsCreate(BaseModel):
    name: str
    eventDate: date  # changed from 'date'
    type: str = Field(..., description="Holiday or Event")
    classes: Optional[list[int]] = None
    preschoolId: int

class HolidaysEventsOut(BaseModel):
    id: int
    name: str
    eventDate: date  # changed from 'date'
    type: str
    classes: Optional[list[int]] = None
    preschoolId: int

    class Config:
        from_attributes = True

class HolidaysEventsUpdate(BaseModel):
    name: Optional[str] = None
    eventDate: Optional[date] = None  # changed from 'date'
    type: Optional[str] = None
    classes: Optional[list[int]] = None