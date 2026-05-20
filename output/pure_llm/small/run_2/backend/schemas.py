from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# Student Schemas
class StudentBase(BaseModel):
    name: str
    email: str

class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None

class StudentResponse(StudentBase):
    id: int
    courses: List["CourseResponse"] = []

    class Config:
        from_attributes = True

# Course Schemas
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

class CourseResponse(CourseBase):
    id: int
    students: List["StudentResponse"] = []
    enrollment_count: int = 0

    class Config:
        from_attributes = True

# Enrollment Schemas
class EnrollmentBase(BaseModel):
    student_id: int
    course_id: int

class EnrollmentCreate(EnrollmentBase):
    pass

class EnrollmentResponse(EnrollmentBase):
    id: int
    enrolled_at: datetime
    student: StudentResponse
    course: CourseResponse

    class Config:
        from_attributes = True

# Update forward references
StudentResponse.model_rebuild()
CourseResponse.model_rebuild()