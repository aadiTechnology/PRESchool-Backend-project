from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.session import Base

class Division(Base):
    __tablename__ = "divisions"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    classId = Column(Integer, ForeignKey("classes.id"), nullable=False)
    preschoolId = Column(Integer, ForeignKey("preschools.id"), nullable=False)