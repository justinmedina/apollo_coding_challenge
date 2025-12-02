from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./vehicles.db"

# Database setup
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  
)

# creates us a database session, and preventing it from reloading, then links engine with our session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for building our database model around
Base = declarative_base()
