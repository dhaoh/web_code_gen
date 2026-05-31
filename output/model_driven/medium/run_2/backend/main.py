"""
FastAPI application entry point for student_course_system_medium.
Generated from model definition.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models import init_db
from routes import routers

app = FastAPI(
    title="Student Course System Medium",
    description="A complete student course selection and management system with users, departments, courses, enrollments, and grades. Teachers manage courses, students enroll and receive grades. ",
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
