from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from typing import Optional

# ---------- Student ----------
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
    model_config = ConfigDict(from_attributes=True)

# ---------- Course ----------
class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None
    capacity: int

class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    capacity: Optional[int] = None

class CourseOut(CourseBase):
    id: int
    enrolled_count: int = 0

    model_config = ConfigDict(from_attributes=True)

# ---------- Enrollment ----------
class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int

class EnrollmentOut(BaseModel):
    id: int
    student_id: int
    course_id: int
    enrolled_at: datetime
    student_name: str
    course_title: str

    model_config = ConfigDict(from_attributes=True)