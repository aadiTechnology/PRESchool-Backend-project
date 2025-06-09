from sqlalchemy import Column, Integer, String
from app.db.session import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    hashed_password = Column(String)
    role = Column(String, default="user")  # <-- Add this line