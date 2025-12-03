# Vehicle Management API — Apollo Engineering Code Challenge

This project implements a Vehicle Management REST API using: FastAPI, SQLite, and SQLAlchemy, and a test suite using pytest.  
The API supports full CRUD operations on vehicle records and includes validation, error handling, and VIN normalization.

# Features

- Create a new vehicle (POST)
- Get a vehicle by VIN (GET)
- Get all vehicles (GET)
- Update a vehicle (PUT)
- Delete a vehicle (DELETE)
- SQLite database with SQLAlchemy ORM
- VIN normalization (all VINs stored as uppercase)
- Full test suite with pytest
- Error handling for:
  - Duplicate VIN (400)
  - Vehicle not found (404)
  - Invalid JSON (422)
  - Invalid field types (422)

# Tech Stack

- Backend API: FastAPI
- Database ORM: SQLAlchemy
- Database: SQLite
- Validation: Pydantic
- Web Server: Uvicorn
- Testing: Pytest + FastAPI TestClient