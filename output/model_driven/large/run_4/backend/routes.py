"""
API routes for student_course_system_large.
Generated from model definition.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from models import (
    User,
    Department,
    Major,
    Course,
    Prerequisite,
    Classroom,
    Schedule,
    CourseSchedule,
    Enrollment,
    Grade,
    Assignment,
    get_session,
)
from schemas import (
    UserCreate,
    UserUpdate,
    UserResponse,
    DepartmentCreate,
    DepartmentUpdate,
    DepartmentResponse,
    MajorCreate,
    MajorUpdate,
    MajorResponse,
    CourseCreate,
    CourseUpdate,
    CourseResponse,
    PrerequisiteCreate,
    PrerequisiteUpdate,
    PrerequisiteResponse,
    ClassroomCreate,
    ClassroomUpdate,
    ClassroomResponse,
    ScheduleCreate,
    ScheduleUpdate,
    ScheduleResponse,
    CourseScheduleCreate,
    CourseScheduleUpdate,
    CourseScheduleResponse,
    EnrollmentCreate,
    EnrollmentUpdate,
    EnrollmentResponse,
    GradeCreate,
    GradeUpdate,
    GradeResponse,
    AssignmentCreate,
    AssignmentUpdate,
    AssignmentResponse,
)

router_1 = APIRouter(prefix="/users", tags=["User"])


@router_1.get("/", response_model=List[UserResponse])
def list_users(session: Session = Depends(get_session)):
    """List all users."""
    items = session.query(User).all()
    return items


@router_1.get("/{item_id}", response_model=UserResponse)
def get_user(item_id: int, session: Session = Depends(get_session)):
    """Get a specific User by ID."""
    item = session.query(User).filter(User.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="User not found")
    return item


@router_1.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(data: UserCreate, session: Session = Depends(get_session)):
    """Create a new User."""
    # Validate create_user logic
    # Check for existing username or email
    existing = session.query(User).filter(
        (User.username == data.username) | (User.email == data.email)
    ).first()
    if existing:
        if existing.username == data.username:
            raise HTTPException(status_code=409, detail="Username already taken")
        else:
            raise HTTPException(status_code=409, detail="Email already taken")
    # Check major existence if provided
    if data.major_id is not None:
        major = session.query(Major).filter(Major.id == data.major_id).first()
        if not major:
            raise HTTPException(status_code=400, detail="Major not found")
    item = User(**data.model_dump())
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@router_1.put("/{item_id}", response_model=UserResponse)
def update_user(item_id: int, data: UserUpdate, session: Session = Depends(get_session)):
    """Update an existing User."""
    item = session.query(User).filter(User.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="User not found")
    # Validate update_user logic
    update_data = data.model_dump(exclude_unset=True)
    # Check for duplicate username if being changed
    if "username" in update_data:
        existing = session.query(User).filter(User.username == update_data["username"], User.id != item_id).first()
        if existing:
            raise HTTPException(status_code=409, detail="Username already taken")
    # Check for duplicate email if being changed
    if "email" in update_data:
        existing = session.query(User).filter(User.email == update_data["email"], User.id != item_id).first()
        if existing:
            raise HTTPException(status_code=409, detail="Email already taken")
    # Check major existence if being set
    if "major_id" in update_data and update_data["major_id"] is not None:
        major = session.query(Major).filter(Major.id == update_data["major_id"]).first()
        if not major:
            raise HTTPException(status_code=400, detail="Major not found")
    for key, value in update_data.items():
        setattr(item, key, value)
    session.commit()
    session.refresh(item)
    return item


@router_1.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(item_id: int, session: Session = Depends(get_session)):
    """Delete a User."""
    item = session.query(User).filter(User.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="User not found")
    # Validate delete_user logic (cascade checks)
    # Check if user is a department head
    dept_as_head = session.query(Department).filter(Department.head_user_id == item_id).first()
    if dept_as_head:
        raise HTTPException(status_code=409, detail="User is set as head of a department; cannot delete")
    # Check if user is teaching any course
    courses_teaching = session.query(Course).filter(Course.teacher_id == item_id).first()
    if courses_teaching:
        raise HTTPException(status_code=409, detail="User is assigned as teacher to courses; cannot delete")
    # Check if user has enrollments
    enrollments = session.query(Enrollment).filter(Enrollment.student_id == item_id).first()
    if enrollments:
        raise HTTPException(status_code=409, detail="User has enrollments; cannot delete")
    session.delete(item)
    session.commit()


router_2 = APIRouter(prefix="/departments", tags=["Department"])


@router_2.get("/", response_model=List[DepartmentResponse])
def list_departments(session: Session = Depends(get_session)):
    """List all departments."""
    items = session.query(Department).all()
    return items


@router_2.get("/{item_id}", response_model=DepartmentResponse)
def get_department(item_id: int, session: Session = Depends(get_session)):
    """Get a specific Department by ID."""
    item = session.query(Department).filter(Department.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Department not found")
    return item


@router_2.post("/", response_model=DepartmentResponse, status_code=status.HTTP_201_CREATED)
def create_department(data: DepartmentCreate, session: Session = Depends(get_session)):
    """Create a new Department."""
    # Validate create_department logic
    # Business rule: head_user_id must be a department head
    if data.head_user_id is not None:
        head = session.query(User).filter(User.id == data.head_user_id).first()
        if not head:
            raise HTTPException(status_code=400, detail="Head user not found")
        if head.role != "department_head":
            raise HTTPException(status_code=400, detail="Head user must have role 'department_head'")
    # Check unique code
    existing = session.query(Department).filter(Department.code == data.code).first()
    if existing:
        raise HTTPException(status_code=409, detail="Department code already exists")
    item = Department(**data.model_dump())
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@router_2.put("/{item_id}", response_model=DepartmentResponse)
def update_department(item_id: int, data: DepartmentUpdate, session: Session = Depends(get_session)):
    """Update an existing Department."""
    item = session.query(Department).filter(Department.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Department not found")
    # Validate update_department logic
    update_data = data.model_dump(exclude_unset=True)
    if "head_user_id" in update_data:
        head_id = update_data["head_user_id"]
        if head_id is not None:
            head = session.query(User).filter(User.id == head_id).first()
            if not head:
                raise HTTPException(status_code=400, detail="Head user not found")
            if head.role != "department_head":
                raise HTTPException(status_code=400, detail="Head user must have role 'department_head'")
    if "code" in update_data:
        existing = session.query(Department).filter(Department.code == update_data["code"], Department.id != item_id).first()
        if existing:
            raise HTTPException(status_code=409, detail="Department code already taken")
    for key, value in update_data.items():
        setattr(item, key, value)
    session.commit()
    session.refresh(item)
    return item


@router_2.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_department(item_id: int, session: Session = Depends(get_session)):
    """Delete a Department."""
    item = session.query(Department).filter(Department.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Department not found")
    # Validate delete_department logic (cascade checks)
    # Check for courses belonging to this department
    courses = session.query(Course).filter(Course.department_id == item_id).first()
    if courses:
        raise HTTPException(status_code=409, detail="Department has courses; cannot delete")
    # Check for majors in this department
    majors = session.query(Major).filter(Major.department_id == item_id).first()
    if majors:
        raise HTTPException(status_code=409, detail="Department has majors; cannot delete")
    session.delete(item)
    session.commit()


router_3 = APIRouter(prefix="/majors", tags=["Major"])


@router_3.get("/", response_model=List[MajorResponse])
def list_majors(session: Session = Depends(get_session)):
    """List all majors."""
    items = session.query(Major).all()
    return items


@router_3.get("/{item_id}", response_model=MajorResponse)
def get_major(item_id: int, session: Session = Depends(get_session)):
    """Get a specific Major by ID."""
    item = session.query(Major).filter(Major.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Major not found")
    return item


@router_3.post("/", response_model=MajorResponse, status_code=status.HTTP_201_CREATED)
def create_major(data: MajorCreate, session: Session = Depends(get_session)):
    """Create a new Major."""
    # Validate create_major logic
    # Check department exists
    dept = session.query(Department).filter(Department.id == data.department_id).first()
    if not dept:
        raise HTTPException(status_code=400, detail="Department not found")
    # Check unique code
    existing = session.query(Major).filter(Major.code == data.code).first()
    if existing:
        raise HTTPException(status_code=409, detail="Major code already exists")
    # total_credits_required positive
    if data.total_credits_required <= 0:
        raise HTTPException(status_code=400, detail="Total credits required must be positive")
    item = Major(**data.model_dump())
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@router_3.put("/{item_id}", response_model=MajorResponse)
def update_major(item_id: int, data: MajorUpdate, session: Session = Depends(get_session)):
    """Update an existing Major."""
    item = session.query(Major).filter(Major.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Major not found")
    # Validate update_major logic
    update_data = data.model_dump(exclude_unset=True)
    if "department_id" in update_data:
        dept = session.query(Department).filter(Department.id == update_data["department_id"]).first()
        if not dept:
            raise HTTPException(status_code=400, detail="Department not found")
    if "code" in update_data:
        existing = session.query(Major).filter(Major.code == update_data["code"], Major.id != item_id).first()
        if existing:
            raise HTTPException(status_code=409, detail="Major code already taken")
    if "total_credits_required" in update_data and update_data["total_credits_required"] <= 0:
        raise HTTPException(status_code=400, detail="Total credits required must be positive")
    for key, value in update_data.items():
        setattr(item, key, value)
    session.commit()
    session.refresh(item)
    return item


@router_3.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_major(item_id: int, session: Session = Depends(get_session)):
    """Delete a Major."""
    item = session.query(Major).filter(Major.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Major not found")
    # Validate delete_major logic (cascade checks)
    # Check if any user is in this major
    users = session.query(User).filter(User.major_id == item_id).first()
    if users:
        raise HTTPException(status_code=409, detail="Major has users assigned; cannot delete")
    session.delete(item)
    session.commit()


router_4 = APIRouter(prefix="/courses", tags=["Course"])


@router_4.get("/", response_model=List[CourseResponse])
def list_courses(session: Session = Depends(get_session)):
    """List all courses."""
    items = session.query(Course).all()
    return items


@router_4.get("/{item_id}", response_model=CourseResponse)
def get_course(item_id: int, session: Session = Depends(get_session)):
    """Get a specific Course by ID."""
    item = session.query(Course).filter(Course.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Course not found")
    return item


@router_4.post("/", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
def create_course(data: CourseCreate, session: Session = Depends(get_session)):
    """Create a new Course."""
    # Many business rules refer to enrollment actions; they are not applicable to course creation.
    # Validate create_course logic
    # Check teacher exists and has role teacher
    teacher = session.query(User).filter(User.id == data.teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=400, detail="Teacher not found")
    if teacher.role != "teacher":
        raise HTTPException(status_code=400, detail="Assigned user is not a teacher")
    # Check department exists
    dept = session.query(Department).filter(Department.id == data.department_id).first()
    if not dept:
        raise HTTPException(status_code=400, detail="Department not found")
    # Check classroom if provided, and capacity constraint
    if data.classroom_id is not None:
        classroom = session.query(Classroom).filter(Classroom.id == data.classroom_id).first()
        if not classroom:
            raise HTTPException(status_code=400, detail="Classroom not found")
        if data.capacity > classroom.capacity:
            raise HTTPException(status_code=400, detail="Course capacity cannot exceed classroom capacity")
    # Unique code check
    existing = session.query(Course).filter(Course.code == data.code).first()
    if existing:
        raise HTTPException(status_code=409, detail="Course code already exists")
    # Capacity positive