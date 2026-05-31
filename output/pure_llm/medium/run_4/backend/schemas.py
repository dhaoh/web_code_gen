from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# User
class UserBase(BaseModel):
    username: str
    role: str
    full_name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None

class UserResponse(UserBase):
    id: int
    password_hash: str  # include? We'll exclude from response later

    class Config:
        orm_mode = True

# Department
class DepartmentBase(BaseModel):
    name: str
    code: str

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentResponse(DepartmentBase):
    id: int

    class Config:
        orm_mode = True

# Course
class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None
    capacity: int
    credits: int
    department_id: int
    teacher_id: Optional[int] = None

class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    capacity: Optional[int] = None
    credits: Optional[int] = None
    department_id: Optional[int] = None
    teacher_id: Optional[int] = None

class CourseResponse(CourseBase):
    id: int

    class Config:
        orm_mode = True

# Enrollment
class EnrollmentBase(BaseModel):
    student_id: int
    course_id: int

class EnrollmentCreate(EnrollmentBase):
    pass

class EnrollmentResponse(EnrollmentBase):
    id: int
    enrolled_at: datetime

    class Config:
        orm_mode = True

# Grade
class GradeBase(BaseModel):
    score: float

class GradeCreate(GradeBase):
    enrollment_id: int

class GradeResponse(GradeBase):
    id: int
    enrollment_id: int
    letter_grade: Optional[str] = None
    graded_at: Optional[datetime] = None

    class Config:
        orm_mode = True

# Assignment
class AssignmentBase(BaseModel):
    course_id: int
    title: str
    description: Optional[str] = None
    due_date: datetime
    max_score: int

class AssignmentCreate(AssignmentBase):
    pass

class AssignmentResponse(AssignmentBase):
    id: int

    class Config:
        orm_mode = True