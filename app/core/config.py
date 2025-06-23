from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str = ""
    SECRET_KEY: str = ""
    ALGORITHM: str = ""
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    SENDGRID_FROM_EMAIL: str = ""
    SENDGRID_API_KEY: str = ""

    class Config:
        env_file = ".env"

settings = Settings()