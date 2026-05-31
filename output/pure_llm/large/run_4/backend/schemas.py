from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime

# User schemas
class UserCreate(BaseModel):
    username: str
    password_hash: str
    role: str
    full_name: str
    email: str
    major_id: Optional[int] = None

class UserUpdate(BaseModel):
    username: Optional[str] = None
    password_hash: Optional[str] = None
    role: Optional[str] = None
    full_name: Optional[str] = None
    email: Optional[str] = None
    major_id: Optional[int] = None

class UserOut(BaseModel):
    id: int
    username: str
    role: str
    full_name: str
    email: str
    major_id: Optional[int]

    class Config:
        orm_mode = True

# Department schemas
class DepartmentCreate(BaseModel):
    name: str
    code: str
    head_user_id: Optional[int] = None

class DepartmentUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    head_user_id: Optional[int] = None

class DepartmentOut(BaseModel):
    id: int
    name: str
    code: str
    head_user_id: Optional[int]

    class Config:
        orm_mode = True

# Major schemas
class MajorCreate(BaseModel):
    name: str
    code: str
    department_id: int
    total_credits_required: int

class MajorUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    department_id: Optional[int] = None
    total_credits_required: Optional[int] = None

class MajorOut(BaseModel):
    id: int
    name: str
    code: str
    department_id: int
    total_credits_required: int

    class Config:
        orm_mode = True

# Classroom schemas
class ClassroomCreate(BaseModel):
    building: str
    room_number: str
    capacity: int

class ClassroomUpdate(BaseModel):
    building: Optional[str] = None
    room_number: Optional[str] = None
    capacity: Optional[int] = None

class ClassroomOut(BaseModel):
    id: int
    building: str
    room_number: str
    capacity: int

    class Config:
        orm_mode = True

# Schedule schemas
class ScheduleCreate(BaseModel):
    day_of_week: int = Field(ge=0, le=6)
    start_time: str = Field(regex=r'^\d{2}:\d{2}$')
    end_time: str = Field(regex=r'^\d{2}:\d{2}$')

class ScheduleUpdate(BaseModel):
    day_of_week: Optional[int] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None

class ScheduleOut(BaseModel):
    id: int
    day_of_week: int
    start_time: str
    end_time: str

    class Config:
        orm_mode = True

# Course schemas
class CourseCreate(BaseModel):
    title: str
    code: str
    description: Optional[str] = None
    capacity: int
    credits: int
    department_id: int
    teacher_id: int
    classroom_id: Optional[int] = None
    semester: str

class CourseUpdate(BaseModel):
    title: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
    capacity: Optional[int] = None
    credits: Optional[int] = None
    department_id: Optional[int] = None
    teacher_id: Optional[int] = None
    classroom_id: Optional[int] = None
    semester: Optional[str] = None

class CourseOut(BaseModel):
    id: int
    title: str
    code: str
    description: Optional[str]
    capacity: int
    credits: int
    department_id: int
    teacher_id: int
    classroom_id: Optional[int]
    semester: str

    class Config:
        orm_mode = True

# Prerequisite schemas
class PrerequisiteCreate(BaseModel):
    course_id: int
    prerequisite_course_id: int
    is_mandatory: bool

class PrerequisiteUpdate(BaseModel):
    is_mandatory: Optional[bool] = None

class PrerequisiteOut(BaseModel):
    id: int
    course_id: int
    prerequisite_course_id: int
    is_mandatory: bool

    class Config:
        orm_mode = True

# Enrollment schemas
class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int

class EnrollmentOut(BaseModel):
    id: int
    student_id: int
    course_id: int
    enrolled_at: datetime
    status: str

    class Config:
        orm_mode = True

# Grade schemas
class GradeCreate(BaseModel):
    enrollment_id: int
    score: float
    letter_grade: Optional[str] = None

class GradeOut(BaseModel):
    id: int
    enrollment_id: int
    score: float
    letter_grade: Optional[str]
    graded_at: Optional[datetime]
    graded_by: Optional[int]

    class Config:
        orm_mode = True

# Assignment schemas
class AssignmentCreate(BaseModel):
    course_id: int
    title: str
    description: Optional[str] = None
    due_date: datetime
    max_score: int

class AssignmentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    max_score: Optional[int] = None

class AssignmentOut(BaseModel):
    id: int
    course_id: int
    title: str
    description: Optional[str]
    due_date: datetime
    max_score: int

    class Config:
        orm_mode = True

# Submission schemas
class SubmissionCreate(BaseModel):
    assignment_id: int
    student_id: int

class SubmissionGrade(BaseModel):
    score: float

class SubmissionOut(BaseModel):
    id: int
    assignment_id: int
    student_id: int
    submitted_at: datetime
    score: Optional[float]
    status: str
    grader_id: Optional[int]

    class Config:
        orm_mode = True

# MajorCourse schemas
class MajorCourseCreate(BaseModel):
    major_id: int
    course_id: int
    is_required: bool = True

class MajorCourseOut(BaseModel):
    id: int
    major_id: int
    course_id: int
    is_required: bool

    class Config:
        orm_mode = True

# Progress response
class CourseProgress(BaseModel):
    course_id: int
    code: str
    title: str
    required: bool
    completed: bool
    grade: Optional[str]

class StudentProgressOut(BaseModel):
    student_id: int
    major_id: Optional[int]
    required_courses: List[CourseProgress]
    total_credits_required: Optional[int]
    earned_credits: int
    progress_percentage: float