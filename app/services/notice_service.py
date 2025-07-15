from sqlalchemy.orm import Session
from app.models.notice import Notice
from app.models.class_ import Class_

def create_notice(db: Session, data, preschool_id: int, user_id: int):
    attachments = ",".join(data.attachments) if data.attachments else None
    notice = Notice(
        title=data.title,
        content=data.content,
        classId=data.classId,
        preschoolId=preschool_id,
        createdBy=user_id,
        date=data.date,
        attachments=attachments,
        divisionId=data.divisionId  # Accept divisionId
    )
    db.add(notice)
    db.commit()
    db.refresh(notice)
    return notice

def update_notice(db: Session, notice: Notice, data):
    for field, value in data.dict(exclude_unset=True).items():
        if field == "attachments" and value is not None:
            setattr(notice, field, ",".join(value))
        elif value is not None:
            setattr(notice, field, value)
    db.commit()
    db.refresh(notice)
    return notice

def delete_notice(db: Session, notice: Notice):
    db.delete(notice)
    db.commit()

def get_notice(db: Session, notice_id: int):
    return db.query(Notice).filter(Notice.id == notice_id).first()

def list_notices_admin(db: Session, preschool_id: int):
    from app.models.class_ import Class_
    notices = (
        db.query(Notice, Class_.name.label("className"))
        .outerjoin(Class_, Notice.classId == Class_.id)
        .filter(Notice.preschoolId == preschool_id)
        .order_by(Notice.date.desc())
        .all()
    )
    result = []
    for notice, className in notices:
        notice_dict = notice.__dict__.copy()
        notice_dict["attachments"] = notice.attachments.split(",") if notice.attachments else []
        notice_dict["className"] = className if className else "All Classes"
        result.append(notice_dict)
    return result

def list_notices_parent(db: Session, preschool_id: int, class_id: int):
    from app.models.class_ import Class_
    notices = (
        db.query(Notice, Class_.name.label("className"))
        .outerjoin(Class_, Notice.classId == Class_.id)
        .filter(
            Notice.preschoolId == preschool_id,
            ((Notice.classId == class_id) | (Notice.classId == None))
        )
        .order_by(Notice.date.desc())
        .all()
    )
    result = []
    for notice, className in notices:
        notice_dict = notice.__dict__.copy()
        notice_dict["attachments"] = notice.attachments.split(",") if notice.attachments else []
        notice_dict["className"] = className if className else "All Classes"
        result.append(notice_dict)
    return result