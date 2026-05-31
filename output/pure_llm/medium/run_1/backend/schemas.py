from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# User
class UserCreate(BaseModel):
    username: str
    password: str
    role: str
    full_name: str
    email: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None
    full_name: Optional[str] = None
    email: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    username: str
    role: str
    full_name: str
    email: str

    class Config:
        orm_mode = True

# Department
class DepartmentCreate(BaseModel):
    name: str
    code: str

class DepartmentResponse(BaseModel):
    id: int
    name: str
    code: str

    class Config:
        orm_mode = True

# Course
class CourseCreate(BaseModel):
    title: str
    description: Optional[str] = None
    capacity: int
    credits: int
    department_id: int
    teacher_id: int

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
    description: Optional[str] = None
    capacity: int
    credits: int
    department_id: int
    teacher_id: int
    department: Optional[DepartmentResponse] = None
    teacher: Optional[UserResponse] = None

    class Config:
        orm_mode = True

# Enrollment
class EnrollmentCreate(BaseModel):
    student_id: int
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

# Grade
class GradeCreate(BaseModel):
    enrollment_id: int
    score: float
    letter_grade: Optional[str] = None

class GradeResponse(BaseModel):
    id: int
    enrollment_id: int
    score: float
    letter_grade: Optional[str] = None
    graded_at: datetime
    enrollment: Optional[EnrollmentResponse] = None

    class Config:
        orm_mode = True

# Assignment
class AssignmentCreate(BaseModel):
    course_id: int
    title: str
    description: Optional[str] = None
    due_date: datetime
    max_score: int

class AssignmentResponse(BaseModel):
    id: int
    course_id: int
    title: str
    description: Optional[str] = None
    due_date: datetime
    max_score: int
    course: Optional[CourseResponse] = None

    class Config:
        orm_mode = True

# Submission
class SubmissionCreate(BaseModel):
    student_id: int
    content: Optional[str] = None
    submitted_at: Optional[datetime] = None

class SubmissionResponse(BaseModel):
    id: int
    assignment_id: int
    student_id: int
    content: Optional[str] = None
    submitted_at: datetime
    is_late: bool
    student: Optional[UserResponse] = None
    assignment: Optional[AssignmentResponse] = None

    class Config:
        orm_mode = True

# Login
class LoginRequest(BaseModel):
    username: str
    password: str