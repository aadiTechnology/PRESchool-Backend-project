from fastapi import APIRouter, Depends, HTTPException, Path, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.notice import NoticeCreate, NoticeUpdate, NoticeOut
from app.services.notice_service import (
    create_notice, update_notice, delete_notice,
    get_notice, list_notices_admin, list_notices_parent
)
from app.models.notice import Notice
from app.utils.security import get_current_user, require_role
from app.core.config import settings
import os
from datetime import datetime

router = APIRouter()

NOTICE_UPLOAD_DIR = "uploads/notices"

@router.post("/notices", response_model=NoticeOut)
async def add_notice(
    title: str = Form(...),
    content: str = Form(...),
    classId: int = Form(None),
    date: str = Form(...),
    attachments: list[UploadFile] = File([]),
    db: Session = Depends(get_db),
    current=Depends(require_role([0, 1, 2]))
):
    tenant_id = str(current["preschoolId"])
    upload_dir = os.path.join(NOTICE_UPLOAD_DIR, tenant_id)
    os.makedirs(upload_dir, exist_ok=True)
    saved_filenames = []
    for file in attachments:
        filename = f"{int(datetime.now().timestamp())}_{file.filename}"
        file_path = os.path.join(upload_dir, filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())
        saved_filenames.append(filename)
    # Prepare a dummy data object for service
    class DummyData:
        pass
    data = DummyData()
    data.title = title
    data.content = content
    data.classId = classId
    data.date = date
    data.attachments = saved_filenames
    notice = create_notice(db, data, preschool_id=current["preschoolId"], user_id=current["id"])
    base_url = f"{settings.API_URL}/{NOTICE_UPLOAD_DIR}/{tenant_id}/"
    notice_dict = notice.__dict__.copy()
    notice_dict["attachments"] = notice.attachments.split(",") if notice.attachments else []
    notice_dict["className"] = "All Classes" if notice.classId is None else None
    notice_dict["baseUrl"] = base_url
    return NoticeOut(**notice_dict)

@router.get("/notices/{notice_id}", response_model=NoticeOut)
def get_notice_api(
    notice_id: int = Path(..., description="The ID of the notice to retrieve"),
    db: Session = Depends(get_db),
    current=Depends(get_current_user)
):
    notice = get_notice(db, notice_id)
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")
    className = "All Classes" if notice.classId is None else None

    notice_dict = notice.__dict__.copy()
    notice_dict["attachments"] = notice.attachments.split(",") if notice.attachments else []
    notice_dict["className"] = className
    tenant_id = str(current["preschoolId"])
    base_url = f"{settings.API_URL}/{NOTICE_UPLOAD_DIR}/{tenant_id}/"
    notice_dict["baseUrl"] = base_url
    return NoticeOut(**notice_dict)

@router.get("/notices", response_model=list[NoticeOut])
def list_notices(
    classId: int = None,
    db: Session = Depends(get_db),
    current=Depends(get_current_user)
):
    tenant_id = str(current["preschoolId"])
    base_url = f"{settings.API_URL}/{NOTICE_UPLOAD_DIR}/{tenant_id}/"
    # Admin: all notices for preschool; Parent: only for their class/all
    if current["role"] in [0, 1, 2]:
        query = db.query(Notice).filter(Notice.preschoolId == current["preschoolId"])
        if classId is not None:
            query = query.filter((Notice.classId == classId) | (Notice.classId == None))
        notices = query.order_by(Notice.date.desc()).all()
        result = []
        for notice in notices:
            notice_dict = notice.__dict__.copy()
            notice_dict["attachments"] = notice.attachments.split(",") if notice.attachments else []
            notice_dict["className"] = "All Classes" if notice.classId is None else None
            notice_dict["baseUrl"] = base_url
            result.append(NoticeOut(**notice_dict))
        return result
    elif current["role"] == 3:
        # For parent, use their classId
        query = db.query(Notice).filter(
            Notice.preschoolId == current["preschoolId"],
            ((Notice.classId == current["classId"]) | (Notice.classId == None))
        )
        notices = query.order_by(Notice.date.desc()).all()
        result = []
        for notice in notices:
            notice_dict = notice.__dict__.copy()
            notice_dict["attachments"] = notice.attachments.split(",") if notice.attachments else []
            notice_dict["className"] = "All Classes" if notice.classId is None else None
            notice_dict["baseUrl"] = base_url
            result.append(notice_dict)
        return [NoticeOut(**n) for n in result]
    else:
        raise HTTPException(status_code=403, detail="Access denied")

@router.get("/notices/{notice_id}", response_model=NoticeOut)
def get_notice_api(
    notice_id: int = Path(..., description="The ID of the notice to retrieve"),
    db: Session = Depends(get_db),
    current=Depends(get_current_user)
):
    notice = get_notice(db, notice_id)
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")
    className = "All Classes" if notice.classId is None else None

    notice_dict = notice.__dict__.copy()
    notice_dict["attachments"] = notice.attachments.split(",") if notice.attachments else []
    notice_dict["className"] = className
    tenant_id = str(current["preschoolId"])
    base_url = f"{settings.API_URL}/{NOTICE_UPLOAD_DIR}/{tenant_id}/"
    notice_dict["baseUrl"] = base_url
    return NoticeOut(**notice_dict)

@router.put("/notices/{notice_id}", response_model=NoticeOut)
async def edit_notice(
    notice_id: int,
    title: str = Form(...),
    content: str = Form(...),
    classId: int = Form(None),
    date: str = Form(...),
    attachments: list[UploadFile] = File([]),
    db: Session = Depends(get_db),
    current=Depends(require_role([0, 1, 2]))  # 0=SuperAdmin, 1=Admin, 2=Teacher)
):
    notice = get_notice(db, notice_id)
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")
    tenant_id = str(current["preschoolId"])
    upload_dir = os.path.join(NOTICE_UPLOAD_DIR, tenant_id)
    os.makedirs(upload_dir, exist_ok=True)
    saved_filenames = []
    for file in attachments:
        filename = f"{int(datetime.now().timestamp())}_{file.filename}"
        file_path = os.path.join(upload_dir, filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())
        saved_filenames.append(filename)
    # Merge with existing attachments
    existing_files = notice.attachments.split(",") if notice.attachments else []
    all_files = existing_files + saved_filenames
    data = NoticeUpdate(
        title=title,
        content=content,
        classId=classId,
        date=date,
        attachments=all_files
    )
    notice = update_notice(db, notice, data)
    base_url = f"{settings.API_URL}/{NOTICE_UPLOAD_DIR}/{tenant_id}/"
    notice_dict = notice.__dict__.copy()
    notice_dict["attachments"] = notice.attachments.split(",") if notice.attachments else []
    notice_dict["className"] = "All Classes" if notice.classId is None else None
    notice_dict["baseUrl"] = base_url
    return NoticeOut(**notice_dict)

@router.delete("/notices/{notice_id}")
def delete_notice_api(
    notice_id: int,
    db: Session = Depends(get_db),
    current=Depends(require_role([0, 1, 2 ]))
):
    notice = get_notice(db, notice_id)
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")
    delete_notice(db, notice)
    return {"message": "Notice deleted"}