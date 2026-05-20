from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime

# Student Schemas
class StudentBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., min_length=5, max_length=100)

class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[str] = Field(None, min_length=5, max_length=100)

class StudentResponse(StudentBase):
    id: int
    
    class Config:
        from_attributes = True

# Course Schemas
class CourseBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    capacity: int = Field(..., gt=0, le=1000)

class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    capacity: Optional[int] = Field(None, gt=0, le=1000)

class CourseResponse(CourseBase):
    id: int
    enrolled_count: int = 0
    
    class Config:
        from_attributes = True

# Enrollment Schemas
class EnrollmentCreate(BaseModel):
    student_id: int = Field(..., gt=0)
    course_id: int = Field(..., gt=0)

class EnrollmentResponse(BaseModel):
    id: int
    student_id: int
    course_id: int
    enrolled_at: datetime
    student_name: str = ""
    course_title: str = ""
    
    class Config:
        from_attributes = True

class EnrollmentListResponse(BaseModel):
    id: int
    student_id: int
    course_id: int
    enrolled_at: datetime
    student_name: str
    course_title: str
    
    class Config:
        from_attributes = True