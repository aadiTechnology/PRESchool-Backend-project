from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime
from app.db.session import Base
import datetime

class Homework(Base):
    __tablename__ = "homeworks"
    id = Column(Integer, primary_key=True, index=True)
    divisionId = Column(Integer, ForeignKey("divisions.id"), nullable=False)  # <-- NEW
    subjectId = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    homeworkDate = Column(Date, nullable=False)
    instructions = Column(String, nullable=False)
    attachments = Column(String, nullable=False)
    teacherId = Column(Integer, ForeignKey("users.id"), nullable=False)
    preschoolId = Column(Integer, ForeignKey("preschools.id"), nullable=False)
    createdAt = Column(DateTime, default=datetime.datetime.utcnow)