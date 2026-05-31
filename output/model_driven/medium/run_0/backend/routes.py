"""
API routes for student_course_system_medium.
Generated from model definition.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from models import (
    User,
    Department,
    Course,
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
    CourseCreate,
    CourseUpdate,
    CourseResponse,
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
    # LLM_FILL: Apply business rule: Only users with role 'student' can enroll in courses. Only users with role 'teacher' can be...
    valid_roles = {'student', 'teacher', 'admin'}
    if data.role not in valid_roles:
        raise HTTPException(status_code=422, detail=f"Invalid role. Allowed roles: {valid_roles}")
    # LLM_FILL: Validate create_user logic
    if session.query(User).filter((User.username == data.username) | (User.email == data.email)).first():
        raise HTTPException(status_code=409, detail="Username or email already exists")
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
    # LLM_FILL: Validate update_user logic
    if data.username and data.username != item.username and session.query(User).filter(User.username == data.username).first():
        raise HTTPException(status_code=409, detail="Username already taken")
    if data.email and data.email != item.email and session.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=409, detail="Email already taken")
    if data.role and data.role not in {'student', 'teacher', 'admin'}:
        raise HTTPException(status_code=422, detail="Invalid role")
    for key, value in data.model_dump(exclude_unset=True).items():
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
    # LLM_FILL: Validate delete_user logic (cascade checks)
    if item.role == 'student' and session.query(Enrollment).filter(Enrollment.student_id == item_id).count() > 0:
        raise HTTPException(status_code=409, detail="Cannot delete student with active enrollments")
    if item.role == 'teacher' and session.query(Course).filter(Course.instructor_id == item_id).count() > 0:
        raise HTTPException(status_code=409, detail="Cannot delete teacher who is assigned to courses")
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
    # LLM_FILL: Validate create_department logic
    if session.query(Department).filter(Department.name == data.name).first():
        raise HTTPException(status_code=409, detail="Department name already exists")
    if session.query(Department).filter(Department.code == data.code).first():
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
    # LLM_FILL: Validate update_department logic
    if data.name and data.name != item.name and session.query(Department).filter(Department.name == data.name).first():
        raise HTTPException(status_code=409, detail="Department name already taken")
    if data.code and data.code != item.code and session.query(Department).filter(Department.code == data.code).first():
        raise HTTPException(status_code=409, detail="Department code already taken")
    for key, value in data.model_dump(exclude_unset=True).items():
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
    # LLM_FILL: Validate delete_department logic (cascade checks)
    if session.query(Course).filter(Course.department_id == item_id).count() > 0:
        raise HTTPException(status_code=409, detail="Cannot delete department that contains courses")
    session.delete(item)
    session.commit()


router_3 = APIRouter(prefix="/courses", tags=["Course"])


@router_3.get("/", response_model=List[CourseResponse])
def list_courses(session: Session = Depends(get_session)):
    """List all courses."""
    items = session.query(Course).all()
    return items


@router_3.get("/{item_id}", response_model=CourseResponse)
def get_course(item_id: int, session: Session = Depends(get_session)):
    """Get a specific Course by ID."""
    item = session.query(Course).filter(Course.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Course not found")
    return item


@router_3.post("/", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
def create_course(data: CourseCreate, session: Session = Depends(get_session)):
    """Create a new Course."""
    # LLM_FILL: Check for existing Enrollment with same keys (duplicate check)
    if session.query(Course).filter(Course.title == data.title, Course.department_id == data.department_id).first():
        raise HTTPException(status_code=409, detail="Course with this title already exists in the department")
    # LLM_FILL: Apply business rule: Prevent enrollment when the course has reached its maximum capacity.
    if data.capacity < 1:
        raise HTTPException(status_code=422, detail="Course capacity must be at least 1")
    if data.credits < 1:
        raise HTTPException(status_code=422, detail="Course credits must be at least 1")
    # LLM_FILL: Apply business rule: Prevent a student from enrolling in the same course more than once.
    # (This rule applies during enrollment creation, not course creation.)

    # LLM_FILL: Apply business rule: Only users with role 'student' can enroll in courses. Only users with role 'teacher' can be...
    if data.instructor_id:
        instructor = session.query(User).filter(User.id == data.instructor_id).first()
        if not instructor:
            raise HTTPException(status_code=404, detail="Instructor not found")
        if instructor.role != 'teacher':
            raise HTTPException(status_code=400, detail="Assigned user must have the 'teacher' role")
    # LLM_FILL: Apply business rule: A student cannot enroll in courses totaling more than 30 credits per semester.
    # (This rule applies during enrollment creation, not course creation.)

    # LLM_FILL: Validate create_course logic
    item = Course(**data.model_dump())
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@router_3.put("/{item_id}", response_model=CourseResponse)
def update_course(item_id: int, data: CourseUpdate, session: Session = Depends(get_session)):
    """Update an existing Course."""
    item = session.query(Course).filter(Course.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Course not found")
    # LLM_FILL: Validate update_course logic
    if data.instructor_id is not None:
        if data.instructor_id != item.instructor_id:
            instructor = session.query(User).filter(User.id == data.instructor_id).first()
            if not instructor:
                raise HTTPException(status_code=404, detail="Instructor not found")
            if instructor.role != 'teacher':
                raise HTTPException(status_code=400, detail="Assigned user must have the 'teacher' role")
    if data.capacity is not None and data.capacity < 1:
        raise HTTPException(status_code=422, detail="Course capacity must be at least 1")
    if data.credits is not None and data.credits < 1:
        raise HTTPException(status_code=422, detail="Course credits must be at least 1")
    if data.title and data.department_id:
        dup = session.query(Course).filter(
            Course.title == data.title,
            Course.department_id == data.department_id,
            Course.id != item_id
        ).first()
        if dup:
            raise HTTPException(status_code=409, detail="Another course with this title already exists in the department")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(item, key, value)
    session.commit()
    session.refresh(item)
    return item


@router_3.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(item_id: int, session: Session = Depends(get_session)):
    """Delete a Course."""
    item = session.query(Course).filter(Course.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Course not found")
    # LLM_FILL: Validate delete_course logic (cascade checks)
    if session.query(Enrollment).filter(Enrollment.course_id == item_id).count() > 0:
        raise HTTPException(status_code=409, detail="Cannot delete course with existing enrollments")
    if session.query(Assignment).filter(Assignment.course_id == item_id).count() > 0:
        raise HTTPException(status_code=409, detail="Cannot delete course with existing assignments")
    session.delete(item)
    session.commit()


router_4 = APIRouter(prefix="/enrollments", tags=["Enrollment"])


@router_4.get("/", response_model=List[EnrollmentResponse])
def list_enrollments(session: Session = Depends(get_session)):
    """List all enrollments."""
    items = session.query(Enrollment).all()
    return items


@router_4.get("/{item_id}", response_model=EnrollmentResponse)
def get_enrollment(item_id: int, session: Session = Depends(get_session)):
    """Get a specific Enrollment by ID."""
    item = session.query(Enrollment).filter(Enrollment.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return item


@router_4.post("/", response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED)
def create_enrollment(data: EnrollmentCreate, session: Session = Depends(get_session)):
    """Create a new Enrollment."""
    # LLM_FILL: Apply business rule: Prevent enrollment when the course has reached its maximum capacity.
    course = session.query(Course).filter(Course.id == data.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    enrollment_count = session.query(Enrollment).filter(Enrollment.course_id == data.course_id).count()
    if enrollment_count >= course.capacity:
        raise HTTPException(status_code=400, detail="Course has reached its maximum capacity")

    # LLM_FILL: Apply business rule: A grade can only be assigned to an existing enrollment. One enrollment can have at most one grade.
    # (This rule applies during grade creation, not enrollment creation.)

    # LLM_FILL: Validate create_enrollment logic
    # Duplicate enrollment check
    if session.query(Enrollment).filter(
        Enrollment.student_id == data.student_id,
        Enrollment.course_id == data.course_id
    ).first():
        raise