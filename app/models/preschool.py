from sqlalchemy import Column, Integer, String
from app.db.session import Base

class Preschool(Base):
    __tablename__ = "preschools"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    city = Column(String, nullable=False)