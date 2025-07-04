from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.db.session import Base
import datetime

class Syllabus(Base):
    __tablename__ = "syllabus"
    id = Column(Integer, primary_key=True, index=True)
    month = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    file_name = Column(String, nullable=False)
    divisionId = Column(Integer, ForeignKey("divisions.id"), nullable=False)
    teacherId = Column(Integer, ForeignKey("users.id"), nullable=False)
    preschoolId = Column(Integer, ForeignKey("preschools.id"), nullable=False)
    createdAt = Column(DateTime, default=datetime.datetime.utcnow)