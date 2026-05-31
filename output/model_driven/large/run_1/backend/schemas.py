"""
Pydantic schemas for student_course_system_large.
Generated from model definition.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

# --- User ---

class UserBase(BaseModel):
    username: str
    password_hash: str
    role: str
    full_name: str
    email: str
    major_id: int | None = None

class UserCreate(UserBase):
    username: str
    password_hash: str
    role: str
    full_name: str
    email: str

class UserUpdate(BaseModel):
    username: str | None = None
    password_hash: str | None = None
    role: str | None = None
    full_name: str | None = None
    email: str | None = None
    major_id: int | None = None

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True


# --- Department ---

class DepartmentBase(BaseModel):
    name: str
    code: str
    head_user_id: int | None = None

class DepartmentCreate(DepartmentBase):
    name: str
    code: str

class DepartmentUpdate(BaseModel):
    name: str | None = None
    code: str | None = None
    head_user_id: int | None = None

class DepartmentResponse(DepartmentBase):
    id: int

    class Config:
        from_attributes = True


# --- Major ---

class MajorBase(BaseModel):
    name: str
    code: str
    department_id: int
    total_credits_required: int = 120

class MajorCreate(MajorBase):
    name: str
    code: str
    department_id: int
    total_credits_required: int = 120

class MajorUpdate(BaseModel):
    name: str | None = None
    code: str | None = None
    department_id: int | None = None
    total_credits_required: int | None = 120

class MajorResponse(MajorBase):
    id: int

    class Config:
        from_attributes = True


# --- Course ---

class CourseBase(BaseModel):
    title: str
    code: str
    description: str | None = None
    capacity: int = 30
    credits: int = 3
    department_id: int
    teacher_id: int
    classroom_id: int | None = None
    semester: str

class CourseCreate(CourseBase):
    title: str
    code: str
    capacity: int = 30
    credits: int = 3
    department_id: int
    teacher_id: int
    semester: str

class CourseUpdate(BaseModel):
    title: str | None = None
    code: str | None = None
    description: str | None = None
    capacity: int | None = 30
    credits: int | None = 3
    department_id: int | None = None
    teacher_id: int | None = None
    classroom_id: int | None = None
    semester: str | None = None

class CourseResponse(CourseBase):
    id: int

    class Config:
        from_attributes = True


# --- Prerequisite ---

class PrerequisiteBase(BaseModel):
    course_id: int
    prerequisite_course_id: int
    is_mandatory: bool = True

class PrerequisiteCreate(PrerequisiteBase):
    course_id: int
    prerequisite_course_id: int
    is_mandatory: bool = True

class PrerequisiteUpdate(BaseModel):
    course_id: int | None = None
    prerequisite_course_id: int | None = None
    is_mandatory: bool | None = True

class PrerequisiteResponse(PrerequisiteBase):
    id: int

    class Config:
        from_attributes = True


# --- Classroom ---

class ClassroomBase(BaseModel):
    building: str
    room_number: str
    capacity: int

class ClassroomCreate(ClassroomBase):
    building: str
    room_number: str
    capacity: int

class ClassroomUpdate(BaseModel):
    building: str | None = None
    room_number: str | None = None
    capacity: int | None = None

class ClassroomResponse(ClassroomBase):
    id: int

    class Config:
        from_attributes = True


# --- Schedule ---

class ScheduleBase(BaseModel):
    day_of_week: int
    start_time: str
    end_time: str

class ScheduleCreate(ScheduleBase):
    day_of_week: int
    start_time: str
    end_time: str

class ScheduleUpdate(BaseModel):
    day_of_week: int | None = None
    start_time: str | None = None
    end_time: str | None = None

class ScheduleResponse(ScheduleBase):
    id: int

    class Config:
        from_attributes = True


# --- CourseSchedule ---

class CourseScheduleBase(BaseModel):
    course_id: int
    schedule_id: int

class CourseScheduleCreate(CourseScheduleBase):
    course_id: int
    schedule_id: int

class CourseScheduleUpdate(BaseModel):
    course_id: int | None = None
    schedule_id: int | None = None

class CourseScheduleResponse(CourseScheduleBase):
    id: int

    class Config:
        from_attributes = True


# --- Enrollment ---

class EnrollmentBase(BaseModel):
    student_id: int
    course_id: int
    enrolled_at: datetime
    status: str = "active"

class EnrollmentCreate(EnrollmentBase):
    student_id: int
    course_id: int
    enrolled_at: datetime
    status: str = "active"

class EnrollmentUpdate(BaseModel):
    student_id: int | None = None
    course_id: int | None = None
    enrolled_at: datetime | None = None
    status: str | None = "active"

class EnrollmentResponse(EnrollmentBase):
    id: int

    class Config:
        from_attributes = True


# --- Grade ---

class GradeBase(BaseModel):
    enrollment_id: int
    score: float
    letter_grade: str | None = None
    graded_at: datetime | None = None
    graded_by: int | None = None

class GradeCreate(GradeBase):
    enrollment_id: int
    score: float

class GradeUpdate(BaseModel):
    enrollment_id: int | None = None
    score: float | None = None
    letter_grade: str | None = None
    graded_at: datetime | None = None
    graded_by: int | None = None

class GradeResponse(GradeBase):
    id: int

    class Config:
        from_attributes = True


# --- Assignment ---

class AssignmentBase(BaseModel):
    course_id: int
    title: str
    description: str | None = None
    due_date: datetime
    max_score: int = 100

class AssignmentCreate(AssignmentBase):
    course_id: int
    title: str
    due_date: datetime
    max_score: int = 100

class AssignmentUpdate(BaseModel):
    course_id: int | None = None
    title: str | None = None
    description: str | None = None
    due_date: datetime | None = None
    max_score: int | None = 100

class AssignmentResponse(AssignmentBase):
    id: int

    class Config:
        from_attributes = True