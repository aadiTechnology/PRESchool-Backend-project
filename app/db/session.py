from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "mssql+pyodbc://@LAPTOP-FC61VAQA\\SQLEXPRESS/erpdb?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"

# engine = create_engine(SQLALCHEMY_DATABASE_URL)
SQLALCHEMY_DATABASE_URL = "mssql+pyodbc://sa:AadiTech123@LAPTOP-FC61VAQA\\SQLEXPRESS/erpdb?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()