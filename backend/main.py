from fastapi import FastAPI
from routers import employee, room, meeting
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

origins = ["http://localhost:3000", "http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=employee.router)
app.include_router(router=room.router)
app.include_router(router=meeting.router)
