"""
Pydantic schemas for student_course_system_small.
Generated from model definition.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


# --- Student ---

class StudentBase(BaseModel):
    name: str    email: str

class StudentCreate(StudentBase):
    name: str
    email: str
    pass


class StudentUpdate(BaseModel):
    name: str    email: str

class StudentResponse(StudentBase):
    id: int

    class Config:
        from_attributes = True


# --- Course ---

class CourseBase(BaseModel):
    title: str    description: str | None = None    capacity: int

class CourseCreate(CourseBase):
    title: str
    capacity: int
    pass


class CourseUpdate(BaseModel):
    title: str    description: str | None = None    capacity: int = 30

class CourseResponse(CourseBase):
    id: int

    class Config:
        from_attributes = True


# --- Enrollment ---

class EnrollmentBase(BaseModel):
    student_id: int    course_id: int    enrolled_at: datetime

class EnrollmentCreate(EnrollmentBase):
    student_id: int
    course_id: int
    enrolled_at: datetime
    pass


class EnrollmentUpdate(BaseModel):
    student_id: int    course_id: int    enrolled_at: datetime = CURRENT_TIMESTAMP

class EnrollmentResponse(EnrollmentBase):
    id: int

    class Config:
        from_attributes = True


