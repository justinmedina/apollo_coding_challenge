from fastapi import FastAPI, Depends
from .database import Base, engine, SessionLocal

app = FastAPI(title="Vehicle Application")

# Create tables on startup
Base.metadata.create_all(bind=engine)

# establish database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
