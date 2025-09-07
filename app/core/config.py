from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str = "mssql+pyodbc://LAPTOP-FC61VAQA\\SQLEXPRESS/erpdb?driver=ODBC+Driver+18+for+SQL+Server&Trusted_Connection=yes&TrustServerCertificate=yes"
    SECRET_KEY: str = ""
    ALGORITHM: str = ""
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    SENDGRID_FROM_EMAIL: str = ""
    SENDGRID_API_KEY: str = ""
    HOMEWORK_UPLOAD_DIR: str = "uploads/homeworks"  # <-- Add this
    API_URL: str = "http://localhost:8000"  # <-- Add this
    
    class Config:
        env_file = ".env"

settings = Settings()