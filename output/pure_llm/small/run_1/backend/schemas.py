from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# Student schemas
class StudentBase(BaseModel):
    name: str = Field(..., min_length=1)
    email: EmailStr

class StudentCreate(StudentBase):
    pass

class StudentUpdate(StudentBase):
    pass

class StudentResponse(StudentBase):
    id: int
    class Config:
        orm_mode = True

# Course schemas
class CourseBase(BaseModel):
    title: str = Field(..., min_length=1)
    description: Optional[str] = None
    capacity: int = Field(..., gt=0)

class CourseCreate(CourseBase):
    pass

class CourseUpdate(CourseBase):
    pass

class CourseResponse(CourseBase):
    id: int
    class Config:
        orm_mode = True

# Enrollment schemas
class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int

class EnrollmentResponse(BaseModel):
    id: int
    student_id: int
    course_id: int
    enrolled_at: datetime
    class Config:
        orm_mode = True