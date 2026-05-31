from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

# Student
class StudentBase(BaseModel):
    name: str
    email: str

class StudentCreate(StudentBase):
    pass

class StudentUpdate(StudentBase):
    pass

class StudentOut(StudentBase):
    id: int
    class Config:
        from_attributes = True

# Course
class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None
    capacity: int = Field(gt=0)

class CourseCreate(CourseBase):
    pass

class CourseUpdate(CourseBase):
    pass

class CourseOut(CourseBase):
    id: int
    enrolled_count: int = 0
    class Config:
        from_attributes = True

# Enrollment
class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int

class EnrollmentOut(BaseModel):
    id: int
    student_id: int
    course_id: int
    enrolled_at: datetime
    class Config:
        from_attributes = True

class EnrollmentDetail(EnrollmentOut):
    student: StudentOut
    course: CourseOut
    class Config:
        from_attributes = True