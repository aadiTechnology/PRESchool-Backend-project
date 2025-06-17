from sqlalchemy.orm import Session
from app.models.holidaysEvents import HolidaysEvents

def createHolidaysEvents(db: Session, data, preschoolId: int):
    classesStr = ",".join(map(str, data.classes)) if data.classes else "All"
    event = HolidaysEvents(
        name=data.name,
        eventDate=data.eventDate,  # changed from 'date'
        type=data.type,
        classes=classesStr,
        preschoolId=preschoolId
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

def updateHolidaysEvents(db: Session, event: HolidaysEvents, data):
    if data.name is not None:
        event.name = data.name
    if data.eventDate is not None:  # changed from 'date'
        event.eventDate = data.eventDate
    if data.type is not None:
        event.type = data.type
    if data.classes is not None:
        event.classes = ",".join(map(str, data.classes))
    db.commit()
    db.refresh(event)
    return event

def deleteHolidaysEvents(db: Session, event: HolidaysEvents):
    db.delete(event)
    db.commit()