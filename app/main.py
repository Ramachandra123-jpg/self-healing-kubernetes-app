import os
import socket
import time

from fastapi import FastAPI, HTTPException, Query

app = FastAPI(
    title="Self-Healing Kubernetes API",
    version="1.0.0"
)

HOSTNAME = socket.gethostname()


@app.get("/")
def home():
    return {
        "message": "Self-Healing Kubernetes Application",
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
    # Development/testing switch for readiness failures.
    if os.path.exists("/tmp/NOT_READY"):
        raise HTTPException(
            status_code=503,
            detail="Application is temporarily not ready"
        )

    return {
        "status": "ready",
        "pod": HOSTNAME
    }


@app.get("/info")
def information():
    return {
        "hostname": HOSTNAME,
        "application": "FastAPI",
        "status": "healthy"
    }


@app.get("/work")
def work(
    ms: int = Query(default=100, ge=1, le=250)
):
    # Deliberately consumes CPU for load-testing purposes.
    end_time = time.perf_counter() + (ms / 1000)

    result = 0

    while time.perf_counter() < end_time:
        result += 1

    return {
        "message": "Work completed",
        "iterations": result,
        "pod": HOSTNAME
    }
