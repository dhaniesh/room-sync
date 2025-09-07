from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Annotated

from database import get_db
from models import Employees
import schema

router = APIRouter(prefix="/employee", tags=["employee"])

db_dependency = Annotated[Session, Depends(get_db)]

@router.get("", response_model=List[schema.Employee])
def get_employee(db: db_dependency):
    employees = db.query(Employees).all()
    return employees


@router.get("/{id}", response_model=schema.Employee)
def get_employee_by_id(id: int, db: db_dependency):
    employee = db.query(Employees).filter(Employees.id == id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@router.post("", response_model=schema.Employee)
def create_employee(
    employee: schema.EmployeeCreate, db: db_dependency
):
    employee_data = Employees(**employee.model_dump())
    db.add(employee_data)
    db.commit()
    db.refresh(employee_data)
    return employee_data
