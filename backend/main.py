from fastapi import FastAPI
from routers import employee, room, meeting

app = FastAPI()

app.include_router(router=employee.router)
app.include_router(router=room.router)
app.include_router(router=meeting.router)
