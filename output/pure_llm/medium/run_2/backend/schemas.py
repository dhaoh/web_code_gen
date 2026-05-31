from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    role: str
    full_name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserResponse(UserBase):
    id: int
    class Config:
        from_attributes = True

class DepartmentBase(BaseModel):
    name: str
    code: str

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentResponse(DepartmentBase):
    id: int
    class Config:
        from_attributes = True

class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None
    capacity: int = Field(gt=0)
    credits: int = Field(gt=0)
    department_id: int
    instructor_id: Optional[int] = None

class CourseCreate(CourseBase):
    pass

class CourseUpdate(CourseBase):
    pass

class CourseResponse(CourseBase):
    id: int
    class Config:
        from_attributes = True

class EnrollmentBase(BaseModel):
    student_id: int
    course_id: int

class EnrollmentCreate(EnrollmentBase):
    pass

class EnrollmentResponse(EnrollmentBase):
    id: int
    enrolled_at: datetime
    class Config:
        from_attributes = True

class GradeBase(BaseModel):
    enrollment_id: int
    score: float

class GradeCreate(GradeBase):
    pass

class GradeUpdate(BaseModel):
    score: float
    letter_grade: Optional[str] = None

class GradeResponse(GradeBase):
    id: int
    letter_grade: Optional[str] = None
    graded_at: Optional[datetime] = None
    class Config:
        from_attributes = True

class AssignmentBase(BaseModel):
    course_id: int
    title: str
    description: Optional[str] = None
    due_date: datetime
    max_score: int = Field(gt=0)

class AssignmentCreate(AssignmentBase):
    pass

class AssignmentUpdate(AssignmentBase):
    pass

class AssignmentResponse(AssignmentBase):
    id: int
    class Config:
        from_attributes = True