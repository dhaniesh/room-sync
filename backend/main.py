from typing import List
from fastapi import FastAPI, status, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import get_db
from models import Employees

app = FastAPI()

@app.get("/employee")
def health(db: Session = Depends(get_db)) -> List[dict]:
    employees = db.query(Employees).all()
    employee_list = []
    for employee in employees:
        employee_list.append({
            "id": employee.id,
            "firstName": employee.firstName,
            "lastName": employee.lastName,
            "email": employee.email
        })
    return JSONResponse(employee_list, status.HTTP_200_OK)

@app.get("/employee/{id}")
def health(id, db: Session = Depends(get_db)) -> List[dict]:
    employee = db.query(Employees).filter(Employees.id == id).first()
    employee = {
        "id": employee.id,
        "firstName": employee.firstName,
        "lastName": employee.lastName,
        "email": employee.email
    }
    return JSONResponse(employee, status.HTTP_200_OK)
