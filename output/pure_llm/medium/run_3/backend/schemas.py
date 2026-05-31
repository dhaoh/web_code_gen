from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    username: str
    full_name: str
    email: EmailStr
    role: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None

class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True

# Department schemas
class DepartmentBase(BaseModel):
    name: str
    code: str

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentUpdate(DepartmentBase):
    pass

class DepartmentResponse(DepartmentBase):
    id: int

    class Config:
        orm_mode = True

# Course schemas
class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None
    capacity: int
    credits: int
    department_id: int
    teacher_id: int

class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    capacity: Optional[int] = None
    credits: Optional[int] = None
    department_id: Optional[int] = None
    teacher_id: Optional[int] = None

class CourseResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    capacity: int
    credits: int
    department_id: int
    teacher_id: int
    department: Optional[DepartmentResponse] = None
    teacher: Optional[UserResponse] = None

    class Config:
        orm_mode = True

# Enrollment schemas
class EnrollmentCreate(BaseModel):
    course_id: int

class EnrollmentResponse(BaseModel):
    id: int
    student_id: int
    course_id: int
    enrolled_at: datetime
    student: Optional[UserResponse] = None
    course: Optional[CourseResponse] = None

    class Config:
        orm_mode = True

# Grade schemas
class GradeCreate(BaseModel):
    enrollment_id: int
    score: float

    @validator('score')
    def score_range(cls, v):
        if v < 0 or v > 100:
            raise ValueError('Score must be between 0 and 100')
        return v

class GradeUpdate(BaseModel):
    score: Optional[float] = None

    @validator('score')
    def score_range(cls, v):
        if v is not None and (v < 0 or v > 100):
            raise ValueError('Score must be between 0 and 100')
        return v

class GradeResponse(BaseModel):
    id: int
    enrollment_id: int
    score: float
    letter_grade: Optional[str]
    graded_at: Optional[datetime]
    enrollment: Optional[EnrollmentResponse] = None

    class Config:
        orm_mode = True

# Assignment schemas
class AssignmentBase(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: datetime
    max_score: int
    course_id: int

class AssignmentCreate(AssignmentBase):
    pass

class AssignmentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    max_score: Optional[int] = None

class AssignmentResponse(AssignmentBase):
    id: int
    course: Optional[CourseResponse] = None

    class Config:
        orm_mode = True