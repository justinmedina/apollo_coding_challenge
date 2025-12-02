from pydantic import BaseModel

class VehicleCreate(BaseModel):
    vin: str
    manufacturer: str
    description: str
    horse_power: int
    model_name: str
    model_year: int
    purchase_price: float
    fuel_type: str


# returning vehicle to client
class VehicleResponse(BaseModel):
    vin: str
    manufacturer: str
    description: str
    horse_power: int
    model_name: str
    model_year: int
    purchase_price: float
    fuel_type: str

    class Config:
        from_attributes = True



