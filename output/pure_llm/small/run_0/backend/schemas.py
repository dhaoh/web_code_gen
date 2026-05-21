from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional, List
from datetime import datetime

# Student schemas
class StudentCreate(BaseModel):
    name: str
    email: EmailStr

class StudentResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True

# Course schemas
class CourseCreate(BaseModel):
    title: str
    description: Optional[str] = None
    capacity: int = Field(..., gt=0)

class CourseResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    capacity: int
    current_enrollment: int = 0  # will be populated dynamically

    class Config:
        from_attributes = True

# Enrollment schemas
class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int

class EnrollmentResponse(BaseModel):
    id: int
    student_id: int
    course_id: int
    enrolled_at: datetime
    student: Optional[StudentResponse] = None
    course: Optional[CourseResponse] = None

    class Config:
        from_attributes = True