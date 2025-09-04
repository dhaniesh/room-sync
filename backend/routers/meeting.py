from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from database import get_db
from models import Meetings
import schema

router = APIRouter(prefix="/meeting", tags=["meeting"])


@router.get("", response_model=List[schema.Meeting])
def get_all_meetings(db: Session = Depends(get_db)):
    meetings = db.query(Meetings).all()
    return meetings


@router.get("/{id}", response_model=schema.Meeting)
def get_meeting_by_id(id: int, db: Session = Depends(get_db)):
    meeting = db.query(Meetings).filter(Meetings.id == id).first()
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    return meeting


@router.post("", response_model=schema.Meeting)
def create_meeting(meeting: schema.MeetingCreate, db: Session = Depends(get_db)):
    start_time_dt = datetime.fromisoformat(meeting.start_time)
    end_time_dt = datetime.fromisoformat(meeting.end_time)

    # Check for overlapping meetings in the same room
    overlapping_meetings = (
        db.query(Meetings)
        .filter(
            Meetings.roomId == meeting.roomId,
            Meetings.start_time < end_time_dt,
            Meetings.end_time > start_time_dt,
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
        start_time=start_time_dt,
        end_time=end_time_dt,
    )
    db.add(db_meeting)
    db.commit()
    db.refresh(db_meeting)
    return db_meeting


@router.put("/{id}", response_model=schema.Meeting)
def update_meeting(id: int, meeting: schema.MeetingCreate, db: Session = Depends(get_db)):
    db_meeting = db.query(Meetings).filter(Meetings.id == id).first()
    if not db_meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")

    start_time_dt = datetime.fromisoformat(meeting.start_time)
    end_time_dt = datetime.fromisoformat(meeting.end_time)

    # Check for overlapping meetings in the same room, excluding the current meeting
    overlapping_meetings = (
        db.query(Meetings)
        .filter(
            Meetings.id != id,  # Exclude the current meeting being updated
            Meetings.roomId == meeting.roomId,
            Meetings.start_time < end_time_dt,
            Meetings.end_time > start_time_dt,
        )
        .first()
    )

    if overlapping_meetings:
        raise HTTPException(
            status_code=400, detail="Room is already booked for the specified time"
        )

    db_meeting.employeeId = meeting.employeeId
    db_meeting.roomId = meeting.roomId
    db_meeting.start_time = start_time_dt
    db_meeting.end_time = end_time_dt
    db.commit()
    db.refresh(db_meeting)
    return db_meeting


@router.delete("/{id}", status_code=204)
def delete_meeting(id: int, db: Session = Depends(get_db)):
    db_meeting = db.query(Meetings).filter(Meetings.id == id).first()
    if not db_meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    db.delete(db_meeting)
    db.commit()
    return {"ok": True}
