import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app, get_db
from app.database import Base
from app import models

TEST_DATABASE_URL = "sqlite:///./test.db"

# setup testdatabase
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}  
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

