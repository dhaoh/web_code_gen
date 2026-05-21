from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime

# ---- Student ----
class StudentBase(BaseModel):
    name: str
    email: EmailStr

class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None

class StudentOut(StudentBase):
    id: int
    class Config:
        orm_mode = True

# ---- Course ----
class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None
    capacity: int = Field(..., gt=0)

class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    capacity: Optional[int] = Field(None, gt=0)

class CourseOut(CourseBase):
    id: int
    class Config:
        orm_mode = True

# ---- Enrollment ----
class EnrollmentBase(BaseModel):
    student_id: int
    course_id: int

class EnrollmentCreate(EnrollmentBase):
    pass

class EnrollmentOut(EnrollmentBase):
    id: int
    enrolled_at: datetime
    student: StudentOut
    course: CourseOut

    class Config:
        orm_mode = True