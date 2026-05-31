"""
Pydantic schemas for student_course_system_medium.
Generated from model definition.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

# --- User ---

class UserBase(BaseModel):
    username: str
    password_hash: str
    role: str
    full_name: str
    email: str

class UserCreate(UserBase):
    username: str
    password_hash: str
    role: str
    full_name: str
    email: str

class UserUpdate(BaseModel):
    username: str | None = None
    password_hash: str | None = None
    role: str | None = None
    full_name: str | None = None
    email: str | None = None

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True


# --- Department ---

class DepartmentBase(BaseModel):
    name: str
    code: str

class DepartmentCreate(DepartmentBase):
    name: str
    code: str

class DepartmentUpdate(BaseModel):
    name: str | None = None
    code: str | None = None

class DepartmentResponse(DepartmentBase):
    id: int

    class Config:
        from_attributes = True


# --- Course ---

class CourseBase(BaseModel):
    title: str
    description: str | None = None
    capacity: int = 30
    credits: int = 3
    department_id: int

class CourseCreate(CourseBase):
    title: str
    capacity: int = 30
    credits: int = 3
    department_id: int

class CourseUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    capacity: int | None = 30
    credits: int | None = 3
    department_id: int | None = None

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


# --- Grade ---

class GradeBase(BaseModel):
    enrollment_id: int
    score: float
    letter_grade: str | None = None
    graded_at: datetime | None = None

class GradeCreate(GradeBase):
    enrollment_id: int
    score: float

class GradeUpdate(BaseModel):
    enrollment_id: int | None = None
    score: float | None = None
    letter_grade: str | None = None
    graded_at: datetime | None = None

class GradeResponse(GradeBase):
    id: int

    class Config:
        from_attributes = True


# --- Assignment ---

class AssignmentBase(BaseModel):
    course_id: int
    title: str
    description: str | None = None
    due_date: datetime
    max_score: int = 100

class AssignmentCreate(AssignmentBase):
    course_id: int
    title: str
    due_date: datetime
    max_score: int = 100

class AssignmentUpdate(BaseModel):
    course_id: int | None = None
    title: str | None = None
    description: str | None = None
    due_date: datetime | None = None
    max_score: int | None = 100

class AssignmentResponse(AssignmentBase):
    id: int

    class Config:
        from_attributes = True