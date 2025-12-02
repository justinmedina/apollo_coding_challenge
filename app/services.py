from sqlalchemy.orm import Session
from . import models, schemas

# CRUD
# Create
# Read
# Update
# Delete

# Create a vehicle
# pydantic -> sql alchemy 
def createVehicle(db:Session, vehicle_data: schemas.VehicleCreate):
    vehicle = models.Vehicle(
        vin=vehicle_data.vin,
        manufacturer=vehicle_data.manufacturer,
        description=vehicle_data.description,
        horse_power=vehicle_data.horse_power,
        model_name=vehicle_data.model_name,
        model_year=vehicle_data.model_year,
        purchase_price=vehicle_data.purchase_price,
        fuel_type=vehicle_data.fuel_type
    )
    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)
    return vehicle


# get a vehicle by VIN
def getVehicle(db:Session, vin:str):
    vehicle = db.query(models.Vehicle).filter(models.Vehicle.vin == vin).first()
    return vehicle

# get all vehicles 
def get_all_vehicles(db:Session):
    return db.query(models.Vehicle).all()