from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class StudentCreate(BaseModel):
    name: str
    email: EmailStr

class StudentUpdate(StudentCreate):
    pass

class StudentResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True

class CourseCreate(BaseModel):
    title: str
    description: Optional[str] = None
    capacity: int = Field(..., gt=0)

class CourseUpdate(CourseCreate):
    pass

class CourseResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    capacity: int
    enrolled_count: Optional[int] = None

    class Config:
        orm_mode = True

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
        orm_mode = True