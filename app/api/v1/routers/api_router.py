from fastapi import APIRouter
from app.api.v1.routers import auth
from app.api.v1.routers import admin
from app.api.v1.routers import login
from app.api.v1.routers import preschool
from app.api.v1.routers import homework
from app.api.v1.routers import subject
from app.api.v1.routers import class_  # <-- Add this import
from app.api.v1.routers import division

api_router = APIRouter()

api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(admin.router, tags=["admin"])
api_router.include_router(login.router, tags=["login"])
api_router.include_router(preschool.router, tags=["preschool"])
api_router.include_router(homework.router, tags=["homework"])
api_router.include_router(subject.router, tags=["subject"])
api_router.include_router(class_.router, tags=["class"])
api_router.include_router(division.router, tags=["division"])