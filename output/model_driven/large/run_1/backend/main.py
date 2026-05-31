"""
FastAPI application entry point for student_course_system_large.
Generated from model definition.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models import init_db
from routes import router

app = FastAPI(
    title="Student Course System Large",
    description="A comprehensive university course management system with users, departments, programs, courses, prerequisites, classrooms, schedules, enrollments, grades, and assignments. ",
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

# Register the single APIRouter from routes
app.include_router(router)


@app.on_event("startup")
def startup():
    init_db()


@app.get("/health")
def health_check():
    return {"status": "ok"}