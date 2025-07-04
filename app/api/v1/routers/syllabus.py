from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Request
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.syllabus import Syllabus
from app.models.division import Division
from app.schemas.syllabus import SyllabusOut
from app.utils.security import require_role, get_current_user
from app.services.syllabus_service import create_syllabus, update_syllabus, delete_syllabus
from app.core.config import settings
import os
from datetime import datetime

router = APIRouter()

SYLLABUS_UPLOAD_DIR = "uploads/syllabus"

@router.post("/syllabus", response_model=SyllabusOut)
async def add_syllabus(
    divisionId: int = Form(...),
    month: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current=Depends(require_role([2]))
):
    year = datetime.now().year
    month_name = datetime.strptime(month, "%m").strftime("%B")
    # Check for duplicate
    existing = db.query(Syllabus).filter(
        Syllabus.divisionId == divisionId,
        Syllabus.month == month,
        Syllabus.year == year,
        Syllabus.preschoolId == current["preschoolId"]
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Syllabus for this month and division already exists.")

    division = db.query(Division).filter(Division.id == divisionId).first()
    if not division:
        raise HTTPException(status_code=404, detail="Division not found")
    division_name = division.name.replace(" ", "_")
    file_ext = os.path.splitext(file.filename)[1]
    file_name = f"{month_name}-{division_name}-{year}{file_ext}"
    tenant_id = str(current["preschoolId"])
    upload_dir = os.path.join(SYLLABUS_UPLOAD_DIR, tenant_id)
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file_name)
    with open(file_path, "wb") as f:
        f.write(await file.read())
    syllabus = create_syllabus(db, month, year, file_name, divisionId, current["id"], current["preschoolId"])
    file_url = f"{settings.API_URL}/uploads/syllabus/{tenant_id}/{file_name}"
    return SyllabusOut(
        id=syllabus.id,
        month=syllabus.month,
        year=syllabus.year,
        file_name=syllabus.file_name,
        divisionId=syllabus.divisionId,
        teacherId=syllabus.teacherId,
        preschoolId=syllabus.preschoolId,
        fileUrl=file_url,
        createdAt=syllabus.createdAt
    )

@router.get("/syllabus", response_model=list[SyllabusOut])
def list_syllabus(
    divisionId: int,
    db: Session = Depends(get_db),
    current=Depends(get_current_user)
):
    tenant_id = str(current["preschoolId"])
    syllabi = db.query(Syllabus).filter(
        Syllabus.divisionId == divisionId,
        Syllabus.preschoolId == current["preschoolId"]
    ).order_by(Syllabus.year.desc(), Syllabus.month.desc()).all()
    result = []
    for s in syllabi:
        file_url = f"{settings.API_URL}/uploads/syllabus/{tenant_id}/{s.file_name}"
        result.append(SyllabusOut(
            id=s.id,
            month=s.month,
            year=s.year,
            file_name=s.file_name,
            divisionId=s.divisionId,
            teacherId=s.teacherId,
            preschoolId=s.preschoolId,
            fileUrl=file_url,
            createdAt=s.createdAt
        ))
    return result

@router.put("/syllabus/{syllabus_id}", response_model=SyllabusOut)
async def edit_syllabus(
    syllabus_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current=Depends(require_role([2]))
):
    syllabus = db.query(Syllabus).filter(Syllabus.id == syllabus_id, Syllabus.teacherId == current["id"]).first()
    if not syllabus:
        raise HTTPException(status_code=404, detail="Syllabus not found")
    tenant_id = str(current["preschoolId"])
    upload_dir = os.path.join(SYLLABUS_UPLOAD_DIR, tenant_id)
    os.makedirs(upload_dir, exist_ok=True)

    # Remove existing file if it exists
    old_file_path = os.path.join(upload_dir, syllabus.file_name)
    if os.path.exists(old_file_path):
        os.remove(old_file_path)

    # Get division name for filename
    division = db.query(Division).filter(Division.id == syllabus.divisionId).first()
    division_name = division.name.replace(" ", "_") if division else "Division"
    month_name = syllabus.month
    year = syllabus.year
    file_ext = os.path.splitext(file.filename)[1]
    new_file_name = f"{month_name}-{division_name}-{year}{file_ext}"
    new_file_path = os.path.join(upload_dir, new_file_name)

    # Save new file
    with open(new_file_path, "wb") as f:
        f.write(await file.read())

    # Update DB record with new file name
    syllabus = update_syllabus(db, syllabus, new_file_name)
    file_url = f"{settings.API_URL}/uploads/syllabus/{tenant_id}/{new_file_name}"
    return SyllabusOut(
        id=syllabus.id,
        month=syllabus.month,
        year=syllabus.year,
        file_name=syllabus.file_name,
        divisionId=syllabus.divisionId,
        teacherId=syllabus.teacherId,
        preschoolId=syllabus.preschoolId,
        fileUrl=file_url,
        createdAt=syllabus.createdAt
    )

@router.delete("/syllabus/{syllabus_id}")
def delete_syllabus_api(
    syllabus_id: int,
    db: Session = Depends(get_db),
    current=Depends(require_role([2]))
):
    syllabus = db.query(Syllabus).filter(Syllabus.id == syllabus_id, Syllabus.teacherId == current["id"]).first()
    if not syllabus:
        raise HTTPException(status_code=404, detail="Syllabus not found")
    tenant_id = str(current["preschoolId"])
    upload_dir = os.path.join(SYLLABUS_UPLOAD_DIR, tenant_id)
    file_path = os.path.join(upload_dir, syllabus.file_name)
    if os.path.exists(file_path):
        os.remove(file_path)
    delete_syllabus(db, syllabus)
    return {"message": "Syllabus deleted"}