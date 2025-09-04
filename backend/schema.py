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
