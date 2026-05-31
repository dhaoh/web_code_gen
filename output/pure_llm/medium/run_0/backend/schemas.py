from pydantic import BaseModel, validator
from typing import Optional, List
from datetime import datetime

# ----- User -----
class UserBase(BaseModel):
    username: str
    role: str
    full_name: str
    email: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None
    full_name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True

# ----- Department -----
class DepartmentBase(BaseModel):
    name: str
    code: str

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentOut(DepartmentBase):
    id: int

    class Config:
        orm_mode = True

# ----- Course -----
class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None
    capacity: int
    credits: int
    department_id: int

class CourseCreate(CourseBase):
    teacher_id: int

class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    capacity: Optional[int] = None
    credits: Optional[int] = None
    department_id: Optional[int] = None
    teacher_id: Optional[int] = None

class CourseOut(CourseBase):
    id: int
    teacher_id: int

    class Config:
        orm_mode = True

# ----- Enrollment -----
class EnrollmentBase(BaseModel):
    student_id: int
    course_id: int

class EnrollmentCreate(EnrollmentBase):
    pass

class EnrollmentOut(BaseModel):
    id: int
    student_id: int
    course_id: int
    enrolled_at: datetime

    class Config:
        orm_mode = True

# ----- Grade -----
class GradeBase(BaseModel):
    score: float

class GradeCreate(GradeBase):
    enrollment_id: int

class GradeUpdate(BaseModel):
    score: Optional[float] = None

class GradeOut(GradeBase):
    id: int
    enrollment_id: int
    letter_grade: Optional[str] = None
    graded_at: Optional[datetime] = None

    class Config:
        orm_mode = True

# ----- Assignment -----
class AssignmentBase(BaseModel):
    course_id: int
    title: str
    description: Optional[str] = None
    due_date: datetime
    max_score: int

class AssignmentCreate(AssignmentBase):
    pass

class AssignmentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    max_score: Optional[int] = None

class AssignmentOut(AssignmentBase):
    id: int

    class Config:
        orm_mode = True

# ----- Submission -----
class SubmissionBase(BaseModel):
    assignment_id: int
    content: Optional[str] = None

class SubmissionCreate(SubmissionBase):
    pass

class SubmissionOut(BaseModel):
    id: int
    assignment_id: int
    student_id: int
    submitted_at: datetime
    content: Optional[str] = None
    is_late: bool

    class Config:
        orm_mode = True

# ----- Auth -----
class Token(BaseModel):
    access_token: str
    token_type: str

class LoginRequest(BaseModel):
    username: str
    password: str