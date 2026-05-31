from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

class StudentBase(BaseModel):
    name: str
    email: str

class StudentCreate(StudentBase):
    pass

class Student(StudentBase):
    id: int

    class Config:
        from_attributes = True

class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None
    capacity: int = Field(..., gt=0, description="Must be positive")

class CourseCreate(CourseBase):
    pass

class Course(CourseBase):
    id: int

    class Config:
        from_attributes = True

class EnrollmentBase(BaseModel):
    student_id: int
    course_id: int

class EnrollmentCreate(EnrollmentBase):
    pass

class EnrollmentRead(BaseModel):
    id: int
    student_id: int
    course_id: int
    enrolled_at: datetime
    student_name: str
    course_title: str

    class Config:
        from_attributes = True