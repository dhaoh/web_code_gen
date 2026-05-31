from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    username: str
    full_name: str
    email: str
    role: str
    major_id: Optional[int] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None
    major_id: Optional[int] = None

class UserOut(UserBase):
    id: int
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# Department schemas
class DepartmentBase(BaseModel):
    name: str
    code: str
    head_user_id: Optional[int] = None

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    head_user_id: Optional[int] = None

class DepartmentOut(DepartmentBase):
    id: int
    class Config:
        from_attributes = True

# Major schemas
class MajorBase(BaseModel):
    name: str
    code: str
    department_id: int
    total_credits_required: int

class MajorCreate(MajorBase):
    pass

class MajorUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    department_id: Optional[int] = None
    total_credits_required: Optional[int] = None

class MajorOut(MajorBase):
    id: int
    class Config:
        from_attributes = True

class MajorCourseCreate(BaseModel):
    major_id: int
    course_id: int

class MajorCourseOut(MajorCourseCreate):
    id: int
    class Config:
        from_attributes = True

# Course schemas
class CourseBase(BaseModel):
    title: str
    code: str
    description: Optional[str] = None
    capacity: int
    credits: int
    department_id: int
    teacher_id: int
    classroom_id: Optional[int] = None
    semester: str

class CourseCreate(CourseBase):
    pass

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

class CourseOut(CourseBase):
    id: int
    class Config:
        from_attributes = True

class PrerequisiteCreate(BaseModel):
    prerequisite_course_id: int
    is_mandatory: bool

class PrerequisiteOut(BaseModel):
    id: int
    course_id: int
    prerequisite_course_id: int
    is_mandatory: bool
    class Config:
        from_attributes = True

# Classroom schemas
class ClassroomBase(BaseModel):
    building: str
    room_number: str
    capacity: int

class ClassroomCreate(ClassroomBase):
    pass

class ClassroomUpdate(BaseModel):
    building: Optional[str] = None
    room_number: Optional[str] = None
    capacity: Optional[int] = None

class ClassroomOut(ClassroomBase):
    id: int
    class Config:
        from_attributes = True

# Schedule schemas
class ScheduleBase(BaseModel):
    day_of_week: int
    start_time: str
    end_time: str

class ScheduleCreate(ScheduleBase):
    pass

class ScheduleUpdate(BaseModel):
    day_of_week: Optional[int] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None

class ScheduleOut(ScheduleBase):
    id: int
    class Config:
        from_attributes = True

class CourseScheduleCreate(BaseModel):
    course_id: int
    schedule_id: int

class CourseScheduleOut(CourseScheduleCreate):
    id: int
    class Config:
        from_attributes = True

# Enrollment schemas
class EnrollmentCreate(BaseModel):
    student_id: int   # will be overridden by current user if student
    course_id: int

class EnrollmentUpdate(BaseModel):
    status: Optional[str] = None

class EnrollmentOut(BaseModel):
    id: int
    student_id: int
    course_id: int
    enrolled_at: datetime
    status: str
    class Config:
        from_attributes = True

# Grade schemas
class GradeCreate(BaseModel):
    enrollment_id: int
    score: float

class GradeOut(BaseModel):
    id: int
    enrollment_id: int
    score: float
    letter_grade: Optional[str] = None
    graded_at: Optional[datetime] = None
    graded_by: Optional[int] = None
    class Config:
        from_attributes = True

# Assignment schemas
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
        from_attributes = True

class AssignmentSubmissionCreate(BaseModel):
    assignment_id: int
    content: Optional[str] = None

class AssignmentSubmissionOut(BaseModel):
    id: int
    assignment_id: int
    student_id: int
    submitted_at: datetime
    content: Optional[str] = None
    score: Optional[float] = None
    late_penalty_applied: bool
    class Config:
        from_attributes = True

class SubmissionGrade(BaseModel):
    score: float