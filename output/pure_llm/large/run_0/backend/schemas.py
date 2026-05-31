from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from .models import User, Department, Major, Course, Prerequisite, Classroom, Schedule, Enrollment, Grade, Assignment, AssignmentSubmission

# ---------- User ----------
class UserCreate(BaseModel):
    username: str
    password: str
    role: str
    full_name: str
    email: str
    major_id: Optional[int] = None

class UserUpdate(BaseModel):
    username: Optional[str] = None
    full_name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None
    major_id: Optional[int] = None

class UserResponse(BaseModel):
    id: int
    username: str
    role: str
    full_name: str
    email: str
    major_id: Optional[int] = None

    class Config:
        orm_mode = True

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

# ---------- Department ----------
class DepartmentCreate(BaseModel):
    name: str
    code: str
    head_user_id: Optional[int] = None

class DepartmentUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    head_user_id: Optional[int] = None

class DepartmentResponse(BaseModel):
    id: int
    name: str
    code: str
    head_user_id: Optional[int] = None

    class Config:
        orm_mode = True

# ---------- Major ----------
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

class MajorResponse(BaseModel):
    id: int
    name: str
    code: str
    department_id: int
    total_credits_required: int

    class Config:
        orm_mode = True

# ---------- Course ----------
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
    schedule_ids: Optional[List[int]] = []  # list of schedule ids to attach

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
    schedule_ids: Optional[List[int]] = None

class CourseResponse(BaseModel):
    id: int
    title: str
    code: str
    description: Optional[str] = None
    capacity: int
    credits: int
    department_id: int
    teacher_id: int
    classroom_id: Optional[int] = None
    semester: str
    schedules: List[int] = []  # list of schedule ids

    @validator("schedules", pre=True, always=True)
    def extract_schedule_ids(cls, v, values, **kwargs):
        if isinstance(v, list):
            return v
        return [s.id for s in v]

    class Config:
        orm_mode = True

# ---------- Prerequisite ----------
class PrerequisiteCreate(BaseModel):
    course_id: int
    prerequisite_course_id: int
    is_mandatory: bool = True

class PrerequisiteResponse(BaseModel):
    id: int
    course_id: int
    prerequisite_course_id: int
    is_mandatory: bool

    class Config:
        orm_mode = True

# ---------- Classroom ----------
class ClassroomCreate(BaseModel):
    building: str
    room_number: str
    capacity: int

class ClassroomResponse(BaseModel):
    id: int
    building: str
    room_number: str
    capacity: int

    class Config:
        orm_mode = True

# ---------- Schedule ----------
class ScheduleCreate(BaseModel):
    day_of_week: int = Field(..., ge=0, le=6)
    start_time: str  # HH:MM
    end_time: str    # HH:MM

class ScheduleResponse(BaseModel):
    id: int
    day_of_week: int
    start_time: str
    end_time: str

    class Config:
        orm_mode = True

# ---------- Enrollment ----------
class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int

class EnrollmentResponse(BaseModel):
    id: int
    student_id: int
    course_id: int
    enrolled_at: datetime
    status: str

    class Config:
        orm_mode = True

# ---------- Grade ----------
class GradeCreate(BaseModel):
    enrollment_id: int
    score: float

class GradeResponse(BaseModel):
    id: int
    enrollment_id: int
    score: float
    letter_grade: Optional[str] = None
    graded_at: Optional[datetime] = None
    graded_by: Optional[int] = None

    class Config:
        orm_mode = True

# ---------- Assignment ----------
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

    class Config:
        orm_mode = True

# ---------- Assignment Submission ----------
class SubmissionCreate(BaseModel):
    assignment_id: int
    student_id: int

class SubmissionUpdate(BaseModel):
    score: Optional[float] = None
    status: Optional[str] = None

class SubmissionResponse(BaseModel):
    id: int
    assignment_id: int
    student_id: int
    submitted_at: datetime
    score: Optional[float] = None
    status: str

    class Config:
        orm_mode = True