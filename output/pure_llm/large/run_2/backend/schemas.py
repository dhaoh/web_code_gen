from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List

class UserBase(BaseModel):
    username: str
    role: str
    full_name: str
    email: str
    major_id: Optional[int] = None

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    class Config:
        orm_mode = True

class DepartmentBase(BaseModel):
    name: str
    code: str
    head_user_id: Optional[int] = None

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentOut(DepartmentBase):
    id: int
    class Config:
        orm_mode = True

class MajorBase(BaseModel):
    name: str
    code: str
    department_id: int
    total_credits_required: int

class MajorCreate(MajorBase):
    pass

class MajorOut(MajorBase):
    id: int
    class Config:
        orm_mode = True

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
    schedule_ids: Optional[List[int]] = []
    prerequisite_ids: Optional[List[int]] = []  # prerequisite course ids

class CourseOut(CourseBase):
    id: int
    class Config:
        orm_mode = True

class PrerequisiteBase(BaseModel):
    course_id: int
    prerequisite_course_id: int
    is_mandatory: bool

class PrerequisiteCreate(PrerequisiteBase):
    pass

class PrerequisiteOut(PrerequisiteBase):
    id: int
    class Config:
        orm_mode = True

class ClassroomBase(BaseModel):
    building: str
    room_number: str
    capacity: int

class ClassroomCreate(ClassroomBase):
    pass

class ClassroomOut(ClassroomBase):
    id: int
    class Config:
        orm_mode = True

class ScheduleBase(BaseModel):
    day_of_week: int
    start_time: str
    end_time: str

class ScheduleCreate(ScheduleBase):
    pass

class ScheduleOut(ScheduleBase):
    id: int
    class Config:
        orm_mode = True

class EnrollmentBase(BaseModel):
    student_id: int
    course_id: int
    status: str = "enrolled"

class EnrollmentCreate(EnrollmentBase):
    pass

class EnrollmentOut(EnrollmentBase):
    id: int
    enrolled_at: datetime
    class Config:
        orm_mode = True

class GradeBase(BaseModel):
    enrollment_id: int
    score: float
    letter_grade: Optional[str] = None
    graded_by: Optional[int] = None

class GradeCreate(GradeBase):
    pass

class GradeOut(GradeBase):
    id: int
    graded_at: Optional[datetime] = None
    class Config:
        orm_mode = True

class AssignmentBase(BaseModel):
    course_id: int
    title: str
    description: Optional[str] = None
    due_date: datetime
    max_score: int

class AssignmentCreate(AssignmentBase):
    pass

class AssignmentOut(AssignmentBase):
    id: int
    class Config:
        orm_mode = True

class SubmissionBase(BaseModel):
    assignment_id: int
    student_id: int

class SubmissionCreate(SubmissionBase):
    pass

class SubmissionOut(SubmissionBase):
    id: int
    submitted_at: datetime
    score: Optional[float] = None
    late: bool = False
    class Config:
        orm_mode = True

class MajorCourseBase(BaseModel):
    major_id: int
    course_id: int
    required: bool = True

class MajorCourseCreate(MajorCourseBase):
    pass

class MajorCourseOut(MajorCourseBase):
    id: int
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class LoginRequest(BaseModel):
    username: str
    password: str