from pydantic import BaseModel


class EmployeeCreate(BaseModel):
    firstName: str
    lastName: str
    email: str

    class Config:
        orm_mode = True


class Employee(EmployeeCreate):
    id: int

    class Config:
        orm_mode = True


class RoomBase(BaseModel):
    name: str


class RoomCreate(RoomBase):
    pass


class Room(RoomBase):
    id: int

    class Config:
        orm_mode = True


from datetime import datetime

class MeetingBase(BaseModel):
    employeeId: int
    roomId: int
    start_time: datetime
    end_time: datetime

    class Config:
        orm_mode = True


class MeetingCreate(MeetingBase):
    pass


class Meeting(MeetingBase):
    id: int

    class Config:
        orm_mode = True
