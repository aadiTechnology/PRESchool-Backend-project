from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password, hashedPassword):
    return pwd_context.verify(plain_password, hashedPassword)

def get_current_user():
    # Dummy implementation: always returns admin
    return {"role": "admin"}
