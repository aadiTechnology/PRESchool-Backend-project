from sqlalchemy import Column, Integer, String, Text, Date, DateTime, ForeignKey
from app.db.session import Base
import datetime

class Notice(Base):
    __tablename__ = "notices"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    classId = Column(Integer, ForeignKey("classes.id"), nullable=True)  # Null = All Classes
    preschoolId = Column(Integer, ForeignKey("preschools.id"), nullable=False)
    createdBy = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(Date, nullable=False)
    attachments = Column(String, nullable=True)  # Comma-separated file URLs
    createdAt = Column(DateTime, default=datetime.datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    divisionId = Column(Integer, ForeignKey("divisions.id"), nullable=True)  # New column