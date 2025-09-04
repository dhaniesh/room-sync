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


class MeetingBase(BaseModel):
    employeeId: int
    roomId: int
    start_time: str
    end_time: str


class MeetingCreate(MeetingBase):
    pass


class Meeting(MeetingBase):
    id: int

    class Config:
        orm_mode = True
