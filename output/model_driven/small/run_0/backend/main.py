"""
FastAPI application entry point for student_course_system_small.
Generated from model definition.
"""
import sys
import subprocess

# Install missing dependencies
try:
    import fastapi
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "fastapi", "uvicorn"])
    from fastapi import FastAPI
else:
    from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from .models import init_db
from .routes import routers

app = FastAPI(
    title="Student Course System Small",
    description="A simple student course selection system. Students can browse available courses and enroll. The system tracks enrollments and prevents over-capacity enrollment.",
    version="1.0.0",
)

# CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all entity routers
for router in routers:
    app.include_router(router)


@app.on_event("startup")
def startup():
    init_db()


@app.get("/health")
def health_check():
    return {"status": "ok"}