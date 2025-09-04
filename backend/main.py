from fastapi import FastAPI
from routers import employee

app = FastAPI()

app.include_router(router=employee.router)
