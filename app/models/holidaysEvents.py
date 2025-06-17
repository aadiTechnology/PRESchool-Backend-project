from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from app.db.session import Base
import datetime

class HolidaysEvents(Base):
    __tablename__ = "holidaysEvents"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    eventDate = Column(Date, nullable=False)  # changed from 'date'
    type = Column(String, nullable=False)
    classes = Column(String, nullable=True)
    preschoolId = Column(Integer, ForeignKey("preschools.id"), nullable=False)
    createdAt = Column(DateTime, default=datetime.datetime.utcnow)