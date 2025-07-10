from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.notice import NoticeCreate, NoticeUpdate, NoticeOut
from app.services.notice_service import (
    create_notice, update_notice, delete_notice,
    get_notice, list_notices_admin, list_notices_parent
)
from app.models.notice import Notice
from app.utils.security import get_current_user, require_role

router = APIRouter()

@router.post("/notices", response_model=NoticeOut)
def add_notice(
    data: NoticeCreate,
    db: Session = Depends(get_db),
    current=Depends(require_role([0, 1, 2]))  # 0=SuperAdmin, 1=Admin
):
    notice = create_notice(db, data, preschool_id=current["preschoolId"], user_id=current["id"])
    return NoticeOut(**notice.__dict__, className="All Classes" if notice.classId is None else None)

@router.get("/notices", response_model=list[NoticeOut])
def list_notices(
    db: Session = Depends(get_db),
    current=Depends(get_current_user)
):
    # Admin: all notices for preschool; Parent: only for their class/all
    if current["role"] in [0, 1]:
        notices = list_notices_admin(db, preschool_id=current["preschoolId"])
    elif current["role"] == 3:
        notices = list_notices_parent(db, preschool_id=current["preschoolId"], class_id=current["classId"])
    else:
        raise HTTPException(status_code=403, detail="Access denied")
    return [NoticeOut(**n) for n in notices]

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

    # Build dict and override attachments
    notice_dict = notice.__dict__.copy()
    notice_dict["attachments"] = notice.attachments.split(",") if notice.attachments else []
    notice_dict["className"] = className
    return NoticeOut(**notice_dict)

@router.put("/notices/{notice_id}", response_model=NoticeOut)
def edit_notice(
    notice_id: int,
    data: NoticeUpdate,
    db: Session = Depends(get_db),
    current=Depends(require_role([0, 1, 2]))  # 0=SuperAdmin, 1=Admin, 2=Teacher)
):
    notice = get_notice(db, notice_id)
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")
    notice = update_notice(db, notice, data)
    className = "All Classes" if notice.classId is None else None

    # Always convert attachments to list for NoticeOut
    notice_dict = notice.__dict__.copy()
    notice_dict["attachments"] = notice.attachments.split(",") if notice.attachments else []
    notice_dict["className"] = className
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