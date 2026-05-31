from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime

# ---------- User ----------
class UserBase(BaseModel):
    username: str
    full_name: str
    email: EmailStr
    role: str
    major_id: Optional[int] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    major_id: Optional[int] = None

class UserOut(UserBase):
    id: int
    class Config:
        orm_mode = True

# ---------- Department ----------
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
        orm_mode = True

# ---------- Major ----------
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
        orm_mode = True

# ---------- Course ----------
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
        orm_mode = True

# ---------- Prerequisite ----------
class PrerequisiteBase(BaseModel):
    course_id: int
    prerequisite_course_id: int
    is_mandatory: bool

class PrerequisiteCreate(PrerequisiteBase):
    pass

class PrerequisiteUpdate(BaseModel):
    is_mandatory: Optional[bool] = None

class PrerequisiteOut(PrerequisiteBase):
    id: int
    class Config:
        orm_mode = True

# ---------- Classroom ----------
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
        orm_mode = True

# ---------- Schedule ----------
class ScheduleBase(BaseModel):
    day_of_week: int
    start_time: str  # HH:MM
    end_time: str    # HH:MM

class ScheduleCreate(ScheduleBase):
    pass

class ScheduleUpdate(BaseModel):
    day_of_week: Optional[int] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None

class ScheduleOut(ScheduleBase):
    id: int
    class Config:
        orm_mode = True

# ---------- Enrollment ----------
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
    status: str
    class Config:
        orm_mode = True

# ---------- Grade ----------
class GradeBase(BaseModel):
    enrollment_id: int
    score: float
    letter_grade: Optional[str] = None

class GradeCreate(GradeBase):
    pass

class GradeOut(GradeBase):
    id: int
    graded_at: Optional[datetime] = None
    graded_by: Optional[int] = None
    class Config:
        orm_mode = True

# ---------- Assignment ----------
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

# ---------- Auth ----------
class Token(BaseModel):
    access_token: str
    token_type: str

class Login(BaseModel):
    username: str
    password: str