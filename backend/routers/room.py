from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Annotated

from database import get_db
from models import Rooms
import schema

router = APIRouter(prefix="/room", tags=["room"])

db_dependency = Annotated[Session, Depends(get_db)]

@router.get("", response_model=List[schema.Room])
def get_all_rooms(db: db_dependency):
    rooms = db.query(Rooms).all()
    return rooms


@router.get("/{id}", response_model=schema.Room)
def get_room_by_id(id: int, db: db_dependency):
    room = db.query(Rooms).filter(Rooms.id == id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room


@router.post("", response_model=schema.Room)
def create_room(room: schema.RoomCreate, db: db_dependency):
    db_room = Rooms(name=room.name)
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room


@router.put("/{id}", response_model=schema.Room)
def update_room(id: int, room: schema.RoomCreate, db: db_dependency):
    db_room = db.query(Rooms).filter(Rooms.id == id).first()
    if not db_room:
        raise HTTPException(status_code=404, detail="Room not found")
    db_room.name = room.name
    db.commit()
    db.refresh(db_room)
    return db_room


@router.delete("/{id}", status_code=204)
def delete_room(id: int, db: db_dependency):
    db_room = db.query(Rooms).filter(Rooms.id == id).first()
    if not db_room:
        raise HTTPException(status_code=404, detail="Room not found")
    db.delete(db_room)
    db.commit()
    return {"ok": True}
