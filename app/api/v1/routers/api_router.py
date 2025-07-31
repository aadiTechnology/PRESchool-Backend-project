from fastapi import APIRouter
from app.api.v1.routers import auth
from app.api.v1.routers import admin
from app.api.v1.routers import login
from app.api.v1.routers import preschool
from app.api.v1.routers import homework
from app.api.v1.routers import subject
from app.api.v1.routers import class_  # <-- Add this import
from app.api.v1.routers import division
from app.api.v1.routers import holidaysEvents  # <-- Add this import
from app.api.v1.routers import notice
from app.api.v1.routers import syllabus
from app.api.v1.routers import attendance
from app.api.v1.routers import my_child_attendance

api_router = APIRouter()

api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(admin.router, tags=["admin"])
api_router.include_router(login.router, tags=["login"])
api_router.include_router(preschool.router, tags=["preschool"])
api_router.include_router(homework.router, tags=["homework"])
api_router.include_router(subject.router, tags=["subject"])
api_router.include_router(class_.router, tags=["class"])
api_router.include_router(division.router, tags=["division"])
api_router.include_router(holidaysEvents.router, tags=["holidaysEvents"])  # <-- Add this line
api_router.include_router(notice.router, tags=["notice"])
api_router.include_router(syllabus.router, tags=["syllabus"])
api_router.include_router(attendance.router, tags=["attendance"])
api_router.include_router(my_child_attendance.router, tags=["my_child_attendance"])