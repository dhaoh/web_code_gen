"""
Pydantic schemas for student_course_system_small.
Generated from model definition.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

# --- Student ---

class StudentBase(BaseModel):
    name: str
    email: str

class StudentCreate(StudentBase):
    name: str
    email: str

class StudentUpdate(BaseModel):
    name: str | None = None
    email: str | None = None

class StudentResponse(StudentBase):
    id: int

    class Config:
        from_attributes = True


# --- Course ---

class CourseBase(BaseModel):
    title: str
    description: str | None = None
    capacity: int = 30

class CourseCreate(CourseBase):
    title: str
    capacity: int = 30

class CourseUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    capacity: int | None = 30

class CourseResponse(CourseBase):
    id: int

    class Config:
        from_attributes = True


# --- Enrollment ---

class EnrollmentBase(BaseModel):
    student_id: int
    course_id: int
    enrolled_at: datetime

class EnrollmentCreate(EnrollmentBase):
    student_id: int
    course_id: int
    enrolled_at: datetime

class EnrollmentUpdate(BaseModel):
    student_id: int | None = None
    course_id: int | None = None
    enrolled_at: datetime | None = None

class EnrollmentResponse(EnrollmentBase):
    id: int

    class Config:
        from_attributes = True