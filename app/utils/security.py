from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.core.config import settings
import random

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password, hashedPassword):
    return pwd_context.verify(plain_password, hashedPassword)

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        role = payload.get("role")
        user_id = payload.get("id")
        preschool_id = payload.get("preschoolId")  # <-- Add this line
        if email is None or role is None or user_id is None or preschool_id is None:
            raise credentials_exception
        return {
            "email": email,
            "role": role,
            "id": user_id,
            "preschoolId": preschool_id  # <-- Add this line
        }
    except JWTError:
        raise credentials_exception

def require_role(required_roles):
    def role_checker(user=Depends(get_current_user)):
        if user["role"] not in required_roles:
            raise HTTPException(status_code=403, detail="Access denied")
        return user
    return role_checker

def generate_otp(length=6):
    import random
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])
