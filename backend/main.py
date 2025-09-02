from typing import List
from fastapi import FastAPI, status, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import get_db
from models import Employees

app = FastAPI()

@app.get("/health")
def health(db: Session = Depends(get_db)) -> List[dict]:
    employees = db.query(Employees).all()
    employee_list = []
    for employee in employees:
        employee_list.append({
            "id": employee.id,
            "uuid": str(employee.uuid),
            "firstName": employee.firstName,
            "lastName": employee.lastName,
            "email": employee.email
        })
    return JSONResponse(employee_list, status.HTTP_200_OK)
