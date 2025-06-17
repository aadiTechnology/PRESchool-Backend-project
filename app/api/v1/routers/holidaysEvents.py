from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.holidaysEvents import HolidaysEvents
from app.schemas.holidaysEvents import HolidaysEventsCreate, HolidaysEventsOut, HolidaysEventsUpdate
from app.utils.security import get_current_user, require_role
from app.services.holidaysEvents_Service import createHolidaysEvents, updateHolidaysEvents, deleteHolidaysEvents

router = APIRouter()

@router.post("/holidaysEvents", response_model=HolidaysEventsOut)
def addHolidaysEvents(
    data: HolidaysEventsCreate,
    db: Session = Depends(get_db),
    current=Depends(require_role([0, 1]))
):
    event = createHolidaysEvents(db, data, data.preschoolId)
    return HolidaysEventsOut(
        id=event.id,
        name=event.name,
        eventDate=event.eventDate,  # changed from 'date'
        type=event.type,
        classes=[int(cid) for cid in event.classes.split(",")] if event.classes and event.classes != "All" else None,
        preschoolId=event.preschoolId
    )

@router.get("/holidaysEvents", response_model=list[HolidaysEventsOut])
def listHolidaysEvents(
    db: Session = Depends(get_db),
    current=Depends(get_current_user)
):
    events = db.query(HolidaysEvents).filter(HolidaysEvents.preschoolId == current["preschoolId"]).all()
    result = []
    for event in events:
        classes = [int(cid) for cid in event.classes.split(",")] if event.classes and event.classes != "All" else None
        result.append(HolidaysEventsOut(
            id=event.id,
            name=event.name,
            eventDate=event.eventDate,  # changed from 'date'
            type=event.type,
            classes=classes,
            preschoolId=event.preschoolId
        ))
    return result

@router.get("/holidaysEvents/{eventId}", response_model=HolidaysEventsOut)
def getHolidaysEvents(
    eventId: int = Path(..., description="The ID of the event to retrieve"),
    db: Session = Depends(get_db),
    current=Depends(get_current_user)
):
    event = db.query(HolidaysEvents).filter(HolidaysEvents.id == eventId).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    classes = [int(cid) for cid in event.classes.split(",")] if event.classes and event.classes != "All" else None
    return HolidaysEventsOut(
        id=event.id,
        name=event.name,
        eventDate=event.eventDate,  # changed from 'date'
        type=event.type,
        classes=classes,
        preschoolId=event.preschoolId
    )

@router.put("/holidaysEvents/{eventId}", response_model=HolidaysEventsOut)
def editHolidaysEvents(
    eventId: int,
    data: HolidaysEventsUpdate,
    db: Session = Depends(get_db),
    current=Depends(require_role([0, 1]))
):
    event = db.query(HolidaysEvents).filter(HolidaysEvents.id == eventId).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    event = updateHolidaysEvents(db, event, data)
    classes = [int(cid) for cid in event.classes.split(",")] if event.classes and event.classes != "All" else None
    return HolidaysEventsOut(
        id=event.id,
        name=event.name,
        eventDate=event.eventDate,  # changed from 'date'
        type=event.type,
        classes=classes,
        preschoolId=event.preschoolId
    )

@router.delete("/holidaysEvents/{eventId}")
def deleteHolidaysEventsApi(
    eventId: int,
    db: Session = Depends(get_db),
    current=Depends(require_role([0, 1]))  # admin only
):
    event = db.query(HolidaysEvents).filter(HolidaysEvents.id == eventId).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    deleteHolidaysEvents(db, event)
    return {"message": "Event deleted"}