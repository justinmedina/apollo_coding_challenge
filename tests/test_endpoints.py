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
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


# ============================================
# TEST 1: POST/Create Vehicle
# ============================================

def test_create_vehicle():
    response = client.post("/vehicle", json={
        "vin": "abc123",
        "manufacturer": "Honda",
        "description": "A solid car",
        "horse_power": 200,
        "model_name": "Civic",
        "model_year": 2020,
        "purchase_price": 20000.00,
        "fuel_type": "Gas"
    })

    assert response.status_code == 201
    data = response.json()
    assert data["vin"] == "ABC123"
    assert data["manufacturer"] == "Honda"

def test_create_duplicate_vehicle():

    client.post("/vehicle", json={
        "vin": "dup001",
        "manufacturer": "Honda",
        "description": "First entry",
        "horse_power": 150,
        "model_name": "Civic",
        "model_year": 2020,
        "purchase_price": 18000,
        "fuel_type": "Gas"
    })

    # Create again with same VIN
    duplicate = client.post("/vehicle", json={
        "vin": "dup001",
        "manufacturer": "Honda",
        "description": "Duplicate",
        "horse_power": 160,
        "model_name": "Civic",
        "model_year": 2021,
        "purchase_price": 19000,
        "fuel_type": "Gas"
    })

    assert duplicate.status_code == 400
    assert duplicate.json()["detail"] == "Vehicle with this VIN already exists"

def test_create_vehicle_invalid_field_type():
    # horse_power is invalid type (string) = 422
    response = client.post("/vehicle", json={
        "vin": "BADTYPE",
        "manufacturer": "Honda",
        "description": "Bad HP",
        "horse_power": "not_a_number",
        "model_name": "Civic",
        "model_year": 2020,
        "purchase_price": 20000,
        "fuel_type": "Gas"
    })

    assert response.status_code == 422

def test_create_vehicle_invalid_json():
    # invalid JSON returns 400
    response = client.post("/vehicle", data="NOT_JSON")
    assert response.status_code == 422


# ============================================
# GET /vehicle/{vin} — GET VEHICLE BY VIN
# ============================================
  
def test_get_vehicle_success():
    client.post("/vehicle", json={
        "vin": "get123",
        "manufacturer": "Toyota",
        "description": "car",
        "horse_power": 150,
        "model_name": "Corolla",
        "model_year": 2015,
        "purchase_price": 15000,
        "fuel_type": "Gas"
    })

    response = client.get("/vehicle/get123")
    assert response.status_code == 200
    assert response.json()["vin"] == "GET123"


def test_get_vehicle_not_found():
    response = client.get("/vehicle/NOEXIST")
    assert response.status_code == 404
    assert response.json()["detail"] == "Vehicle not found"


# ============================================
# GET /vehicle — GET ALL VEHICLES
# ============================================

def test_get_all_vehicles():
    response = client.get("/vehicle")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# ============================================
# PUT /vehicle/{vin} — UPDATE VEHICLE
# ============================================
    
def test_update_vehicle_success():
    # first Create 
    client.post("/vehicle", json={
        "vin": "upd123",
        "manufacturer": "Ford",
        "description": "Old desc",
        "horse_power": 120,
        "model_name": "Focus",
        "model_year": 2018,
        "purchase_price": 10000,
        "fuel_type": "Gas"
    })

    # now Update
    response = client.put("/vehicle/upd123", json={
        "vin": "upd123",
        "manufacturer": "Ford",
        "description": "Updated desc",
        "horse_power": 140,
        "model_name": "Focus SE",
        "model_year": 2019,
        "purchase_price": 11000,
        "fuel_type": "Gas"
    })

    assert response.status_code == 200
    assert response.json()["description"] == "Updated desc"
    assert response.json()["horse_power"] == 140


def test_update_vehicle_not_found():
    response = client.put("/vehicle/NONE999", json={
        "vin": "NONE999",
        "manufacturer": "boo",
        "description": "blah",
        "horse_power": 100,
        "model_name": "NA",
        "model_year": 2020,
        "purchase_price": 10000,
        "fuel_type": "welp"
    })

    assert response.status_code == 404
    assert response.json()["detail"] == "Vehicle not found"
