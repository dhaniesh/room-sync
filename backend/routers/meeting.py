from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Annotated
from datetime import datetime

from database import get_db
from models import Meetings
import schema

router = APIRouter(prefix="/meeting", tags=["meeting"])

db_dependency = Annotated[Session, Depends(get_db)]

@router.get("", response_model=List[schema.Meeting])
def get_all_meetings(db: db_dependency):
    meetings = db.query(Meetings).all()
    return meetings


@router.get("/{id}", response_model=schema.Meeting)
def get_meeting_by_id(id: int, db: db_dependency):
    meeting = db.query(Meetings).filter(Meetings.id == id).first()
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    return meeting


@router.post("", response_model=schema.Meeting)
def create_meeting(meeting: schema.MeetingCreate, db: db_dependency):
    # Check for overlapping meetings in the same room
    overlapping_meetings = (
        db.query(Meetings)
        .filter(
            Meetings.roomId == meeting.roomId,
            Meetings.start_time < meeting.end_time,
            Meetings.end_time > meeting.start_time,
        )
        .first()
    )

    if overlapping_meetings:
        raise HTTPException(
            status_code=400, detail="Room is already booked for the specified time"
        )

    db_meeting = Meetings(
        employeeId=meeting.employeeId,
        roomId=meeting.roomId,
        start_time=meeting.start_time,
        end_time=meeting.end_time,
    )
    db.add(db_meeting)
    db.commit()
    db.refresh(db_meeting)
    return db_meeting


@router.put("/{id}", response_model=schema.Meeting)
def update_meeting(id: int, meeting: schema.MeetingCreate, db: db_dependency):
    db_meeting = db.query(Meetings).filter(Meetings.id == id).first()
    if not db_meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")

    # Check for overlapping meetings in the same room, excluding the current meeting
    overlapping_meetings = (
        db.query(Meetings)
        .filter(
            Meetings.id != id,  # Exclude the current meeting being updated
            Meetings.roomId == meeting.roomId,
            Meetings.start_time < meeting.end_time,
            Meetings.end_time > meeting.start_time,
        )
        .first()
    )

    if overlapping_meetings:
        raise HTTPException(
            status_code=400, detail="Room is already booked for the specified time"
        )

    db_meeting.employeeId = meeting.employeeId
    db_meeting.roomId = meeting.roomId
    db_meeting.start_time = meeting.start_time
    db_meeting.end_time = meeting.end_time
    db.commit()
    db.refresh(db_meeting)
    return db_meeting


@router.delete("/{id}", status_code=204)
def delete_meeting(id: int, db: db_dependency):
    db_meeting = db.query(Meetings).filter(Meetings.id == id).first()
    if not db_meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    db.delete(db_meeting)
    db.commit()
    return {"ok": True}
