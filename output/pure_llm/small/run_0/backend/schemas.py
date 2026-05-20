from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime

# Student Schemas
class StudentBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., min_length=5, max_length=100)

    @validator('email')
    def validate_email(cls, v):
        if '@' not in v or '.' not in v:
            raise ValueError('Invalid email format')
        return v

class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[str] = Field(None, min_length=5, max_length=100)

    @validator('email')
    def validate_email(cls, v):
        if v is not None and ('@' not in v or '.' not in v):
            raise ValueError('Invalid email format')
        return v

class StudentResponse(StudentBase):
    id: int
    courses: List['CourseResponse'] = []

    class Config:
        from_attributes = True

# Course Schemas
class CourseBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=500)
    capacity: int = Field(..., ge=1, le=1000)

class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=500)
    capacity: Optional[int] = Field(None, ge=1, le=1000)

class CourseResponse(CourseBase):
    id: int
    students: List['StudentResponse'] = []
    enrolled_count: int = 0

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
    student: Optional[StudentResponse] = None
    course: Optional[CourseResponse] = None

    class Config:
        from_attributes = True

class EnrollmentError(BaseModel):
    detail: str
    error_code: str

# Update forward references
StudentResponse.model_rebuild()
CourseResponse.model_rebuild()