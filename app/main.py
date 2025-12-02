from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import Base, engine, SessionLocal
from . import services, schemas

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

#endpoints

# create vehicle
@app.post("/vehicle", response_model=schemas.VehicleResponse, status_code=201)
def create_vehicle(vehicle: schemas.VehicleCreate, db: Session = Depends(get_db)):
    existing_vehicle = services.getVehicle(db, vehicle.vin)
    if existing_vehicle:
        raise HTTPException(status_code=400, detail="Vehicle with this VIN already exists")
    return services.createVehicle(db, vehicle)

# get a vehicle
@app.get("/vehicle/{vin}", response_model=schemas.VehicleResponse, status_code=200)
def get_vehicle(vin: str, db: Session = Depends(get_db)):
    vehicle = services.getVehicle(db, vin)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle
