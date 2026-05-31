from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routes import (
    auth_router,
    users_router,
    departments_router,
    majors_router,
    courses_router,
    prerequisites_router,
    classrooms_router,
    schedules_router,
    enrollments_router,
    grades_router,
    assignments_router,
    submissions_router
)

app = FastAPI(title="Student Course System")

origins = [
    "http://localhost:3000",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(departments_router, prefix="/departments", tags=["departments"])
app.include_router(majors_router, prefix="/majors", tags=["majors"])
app.include_router(courses_router, prefix="/courses", tags=["courses"])
app.include_router(prerequisites_router, prefix="/prerequisites", tags=["prerequisites"])
app.include_router(classrooms_router, prefix="/classrooms", tags=["classrooms"])
app.include_router(schedules_router, prefix="/schedules", tags=["schedules"])
app.include_router(enrollments_router, prefix="/enrollments", tags=["enrollments"])
app.include_router(grades_router, prefix="/grades", tags=["grades"])
app.include_router(assignments_router, prefix="/assignments", tags=["assignments"])
app.include_router(submissions_router, prefix="/submissions", tags=["submissions"])