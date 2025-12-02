from sqlalchemy import Column, String, Integer, Float
from .database import Base

# database model is like a row in a table
class Vehicle(Base):
    __tablename__ = "vehicles"

    vin = Column(String, primary_key=True, index=True)
    manufacturer = Column(String, nullable=False)
    description = Column(String, nullable=False)
    horse_power = Column(Integer, nullable=False)
    model_name = Column(String, nullable=False)
    model_year = Column(Integer, nullable=False)
    purchase_price = Column(Float, nullable=False)
    fuel_type = Column(String, nullable=False)
