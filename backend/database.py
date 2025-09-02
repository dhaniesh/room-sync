from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB = "postgresql+psycopg2://postgres:password@localhost:5432/roomsync"

engine = create_engine(DB)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
