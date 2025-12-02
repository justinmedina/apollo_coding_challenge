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
    vehicle.vin = vehicle.vin.upper()
    existing_vehicle = services.get_vehicle(db, vehicle.vin)
    if existing_vehicle:
        raise HTTPException(status_code=400, detail="Vehicle with this VIN already exists")
    return services.create_vehicle(db, vehicle)

# get a vehicle by vin
@app.get("/vehicle/{vin}", response_model=schemas.VehicleResponse, status_code=200)
def get_vehicle(vin: str, db: Session = Depends(get_db)):
    vin = vin.upper()
    vehicle = services.get_vehicle(db, vin)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle

# get a list of all vehicles
@app.get("/vehicle",response_model=list[schemas.VehicleResponse], status_code=200)
def get_all_vehicles(db: Session = Depends(get_db)):
    return services.get_all_vehicles(db)

# update a vehicle
@app.put("/vehicle/{vin}", response_model=schemas.VehicleResponse,status_code=200)
def update_vehicle(vin: str, vehicle: schemas.VehicleCreate, db:Session = Depends(get_db)):
    vin = vin.upper()
    updated_vehicle = services.update_vehicle(db, vin, vehicle)
    if not updated_vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return updated_vehicle

@app.delete("/vehicle/{vin}",status_code=204)
def delete_vehicle(vin:str, db: Session = Depends(get_db)):
    vin = vin.upper()
    deleted_vehicle = services.delete_vehicle(db, vin)
    if not deleted_vehicle: 
        raise HTTPException(status_code=404,detail="Vehicle not found")
    
    return





