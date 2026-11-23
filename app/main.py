
import os
import socket
import time

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Query, Depends
from pydantic import BaseModel, ConfigDict, Field

from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from database import Base, engine, get_db
from models import Employee


HOSTNAME = socket.gethostname()


# Create database tables when the application starts.
@asynccontextmanager
async def lifespan(app: FastAPI):

    for attempt in range(30):
        try:
            Base.metadata.create_all(bind=engine)
            print("Database connection successful")
            break

        except SQLAlchemyError:
            if attempt == 29:
                raise

            print("Waiting for PostgreSQL...")
            time.sleep(2)

    yield


app = FastAPI(
    title="Self-Healing Kubernetes API",
    version="2.0.0",
    lifespan=lifespan
)


# Request schema
class EmployeeCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    department: str = Field(min_length=1, max_length=100)


# Response schema
class EmployeeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    department: str


@app.get("/")
def home():
    return {
        "message": "Self-Healing Kubernetes Application",
        "version": "2.0.0",
        "status": "running",
        "pod": HOSTNAME
    }


@app.get("/health/live")
def liveness():
    return {
        "status": "alive",
        "pod": HOSTNAME
    }


@app.get("/health/ready")
def readiness():

    if os.path.exists("/tmp/NOT_READY"):
        raise HTTPException(
            status_code=503,
            detail="Application is temporarily not ready"
        )

    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "status": "ready",
            "database": "connected",
            "pod": HOSTNAME
        }

    except SQLAlchemyError:
        raise HTTPException(
            status_code=503,
            detail="Database is unavailable"
        )


@app.get("/info")
def information():
    return {
        "hostname": HOSTNAME,
        "application": "FastAPI",
        "database": "PostgreSQL",
        "status": "healthy"
    }


@app.get("/work")
def work(
    ms: int = Query(default=100, ge=1, le=250)
):

    end_time = time.perf_counter() + (ms / 1000)

    result = 0

    while time.perf_counter() < end_time:
        result += 1

    return {
        "message": "Work completed",
        "iterations": result,
        "pod": HOSTNAME
    }


# CREATE EMPLOYEE
@app.post(
    "/employees",
    response_model=EmployeeResponse,
    status_code=201
)
def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db)
):

    new_employee = Employee(
        name=employee.name,
        department=employee.department
    )

    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)

    return new_employee


# GET ALL EMPLOYEES
@app.get("/employees")
def get_employees(db: Session = Depends(get_db)):

    return db.query(Employee).all()


# GET EMPLOYEE BY ID
@app.get("/employees/{employee_id}")
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):

    employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return employee


# DELETE EMPLOYEE
@app.delete("/employees/{employee_id}")
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):

    employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    db.delete(employee)
    db.commit()

    return {
        "message": "Employee deleted successfully",
        "employee_id": employee_id
    }

