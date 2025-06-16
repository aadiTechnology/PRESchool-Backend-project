from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.session import Base

class Class_(Base):
    __tablename__ = "classes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    preschoolId = Column(Integer, ForeignKey("preschools.id"), nullable=False)