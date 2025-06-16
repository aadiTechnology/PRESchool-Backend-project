from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from app.db.session import Base
import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    firstName = Column(String)
    lastName = Column(String)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    hashedPassword = Column(String)
    role = Column(String, default="user")
    preschoolId = Column(Integer, ForeignKey("preschools.id"))
    classId = Column(Integer, ForeignKey("classes.id"), nullable=True)
    divisionId = Column(Integer, ForeignKey("divisions.id"), nullable=True)
    # Teacher fields
    qualification = Column(String, nullable=True)
    # Parent fields
    childName = Column(String, nullable=True)
    childAge = Column(Integer, nullable=True)
    childClass = Column(String, nullable=True)
    otp = Column(String, nullable=True)
    otpExpiry = Column(DateTime, nullable=True)