from sqlalchemy import Column, Integer, Date, DateTime, String, ForeignKey
from app.db.session import Base
import datetime

class Attendance(Base):
    __tablename__ = "attendances"
    id = Column(Integer, primary_key=True, index=True)
    userId = Column(Integer, ForeignKey("users.id"), nullable=False)
    divisionId = Column(Integer, ForeignKey("divisions.id"), nullable=False)
    scanTime = Column(DateTime, nullable=True)
    date = Column(Date, nullable=False)
    status = Column(String, nullable=False)  # "Present" or "Absent"
    createdAt = Column(DateTime, default=datetime.datetime.utcnow)