from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Employees(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    firstName = Column(String(50), nullable=False)
    lastName = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)

    meetings = relationship("Meetings", back_populates="employee")


class Rooms(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    meetings = relationship("Meetings", back_populates="room")


class Meetings(Base):
    __tablename__ = "meetings"

    id = Column(Integer, primary_key=True)
    employeeId = Column(Integer, ForeignKey("employees.id"), nullable=False)
    roomId = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)

    # Relationships for easier ORM querying
    employee = relationship("Employees", back_populates="meetings")
    room = relationship("Rooms", back_populates="meetings")
