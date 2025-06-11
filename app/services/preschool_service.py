from sqlalchemy.orm import Session
from app.models.preschool import Preschool
from app.models.user import User
from app.utils.security import get_password_hash
import random
import string

def generate_password(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def create_preschool_with_admin(db: Session, data):
    # Create preschool
    preschool = Preschool(name=data.preschoolName, city=data.city)
    db.add(preschool)
    db.flush()  # get preschool.id

    # Generate password if not provided
    password = data.initial_password or generate_password()
    hashedPassword = get_password_hash(password)

    # Create admin user with preschoolId
    admin_user = User(
        firstName=data.adminFirstName,
        lastName=data.adminLastName,
        email=data.adminEmail,
        phone=data.adminPhone,
        hashedPassword=hashedPassword,
        role=1,
        preschoolId=preschool.id  # <-- set the foreign key here
    )
    db.add(admin_user)
    db.commit()
    db.refresh(preschool)
    db.refresh(admin_user)
    return preschool, admin_user, password