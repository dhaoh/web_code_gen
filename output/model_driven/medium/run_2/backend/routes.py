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
    # Ensure the role is one of the allowed system roles
    ALLOWED_ROLES = {'student', 'teacher', 'admin'}
    if data.role not in ALLOWED_ROLES:
        raise HTTPException(status_code=422, detail=f"Invalid role. Allowed roles: {ALLOWED_ROLES}")
    # LLM_FILL: Validate create_user logic
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
    # If role is being changed, validate the new role
    if data.role is not None:
        ALLOWED_ROLES = {'student', 'teacher', 'admin'}
        if data.role not in ALLOWED_ROLES:
            raise HTTPException(status_code=422, detail=f"Invalid role. Allowed roles: {ALLOWED_ROLES}")
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
    # Prevent deletion if user is a student with active enrollments or is an instructor for any course
    if item.role == 'student':
        has_enrollments = session.query(Enrollment).filter(Enrollment.student_id == item_id).first()
        if has_enrollments:
            raise HTTPException(status_code=400, detail="Cannot delete user with existing enrollments")
    if item.role == 'teacher':
        has_courses = session.query(Course).filter(Course.teacher_id == item_id).first()
        if has_courses:
            raise HTTPException(status_code=400, detail="Cannot delete teacher who is assigned to courses")
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
    # No additional business rules for department creation
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
    # No additional business rules for department updates
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
    # Prevent deletion if department has courses
    courses_count = session.query(Course).filter(Course.department_id == item_id).count()
    if courses_count > 0:
        raise HTTPException(status_code=400, detail="Cannot delete department with existing courses")
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
    # Not applicable for course creation – duplicate enrollments are checked during enrollment creation

    # LLM_FILL: Apply business rule: Prevent enrollment when the course has reached its maximum capacity.
    # Not applicable for course creation – capacity is checked during enrollment creation

    # LLM_FILL: Apply business rule: Prevent a student from enrolling in the same course more than once.
    # Not applicable for course creation

    # LLM_FILL: Apply business rule: Only users with role 'student' can enroll in courses. Only users with role 'teacher' can be...
    # Enforce that the teacher/instructor is a user with the 'teacher' role
    if hasattr(data, 'teacher_id') and data.teacher_id is not None:
        instructor = session.query(User).filter(User.id == data.teacher_id).first()
        if not instructor or instructor.role != 'teacher':
            raise HTTPException(status_code=400, detail="Instructor must be a user with role 'teacher'")

    # LLM_FILL: Apply business rule: A student cannot enroll in courses totaling more than 30 credits per semester.
    # Not applicable here – credit limits are checked during enrollment creation

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
    # If teacher is being updated, ensure the new teacher has the correct role
    if hasattr(data, 'teacher_id') and data.teacher_id is not None:
        instructor = session.query(User).filter(User.id == data.teacher_id).first()
        if not instructor or instructor.role != 'teacher':
            raise HTTPException(status_code=400, detail="Instructor must be a user with role 'teacher'")
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
    # Prevent deletion if course has enrollments
    enrollments_count = session.query(Enrollment).filter(Enrollment.course_id == item_id).count()
    if enrollments_count > 0:
        raise HTTPException(status_code=400, detail="Cannot delete course with existing enrollments")
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
    # Check student role
    student = session.query(User).filter(User.id == data.student_id).first()
    if not student or student.role != 'student':
        raise HTTPException(status_code=400, detail="Only users with role 'student' can enroll in courses")

    # Fetch course
    course = session.query(Course).filter(Course.id == data.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # Capacity check: count current enrollments for this course
    current_count = session.query(Enrollment).filter(Enrollment.course_id == data.course_id).count()
    if current_count >= course.capacity:
        raise HTTPException(status_code=409, detail="Course has reached maximum capacity")

    # Duplicate enrollment check
    existing = session.query(Enrollment).filter(
        Enrollment.student_id == data.student_id,
        Enrollment.course_id == data.course_id
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail="Student is already enrolled in this course")

    # Credit limit: total credits from all courses the student is enrolled in plus this new course must not exceed 30
    student_enrollments = session.query(Enrollment).filter(Enrollment.student_id == data.student_id).all()
    total_credits = 0
    for enrollment in student_enrollments:
        enrolled_course = session.query(Course).filter(Course.id == enrollment.course_id).first()
        if enrolled_course:
            total_credits += enrolled_course.credits
    if total_credits + course.credits > 30:
        raise HTTPException(status_code=400, detail="Enrolling in this course would exceed the 30-credit limit")

    # LLM_FILL: Apply business rule: A grade can only be assigned to an existing enrollment. One enrollment can have at most one grade.
    # Not needed during enrollment creation – this rule applies to grade creation

    # LLM_FILL: Validate create_enrollment logic
    item = Enrollment(**data.model_dump())
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@router_4.put("/{item_id}", response_model=EnrollmentResponse)
def update_enrollment(item_id: int, data: EnrollmentUpdate, session: Session = Depends(get_session)):
    """Update an existing Enrollment."""
    item = session.query(Enrollment).filter(Enrollment.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    # LLM_FILL: Validate update_enrollment logic
    # No additional business rules for enrollment updates (changing enrollment is unusual, but we respect existing logic)
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(item, key, value)
    session.commit()
    session.refresh(item)
    return item


@router_4.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_enrollment(item_id: int, session: Session = Depends(get_session)):
    """Delete a Enrollment."""
    item = session.query(Enrollment).filter(Enrollment.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    # LLM_FILL: Validate delete_enrollment logic (cascade checks)
    # Prevent deletion if the enrollment already has a grade (cascade constraint)
    existing_grade = session.query(Grade).filter(Grade.enrollment_id == item_id).first()
    if existing_grade:
        raise HTTPException(status_code=400, detail="Cannot delete enrollment that already has a grade")
    session.delete(item)
    session.commit()


router_5 = APIRouter(prefix="/grades", tags=["Grade"])


@router_5.get("/", response_model=List[GradeResponse])
def list_grades(session: Session = Depends(get_session)):
    """List all grades."""
    items = session.query(Grade).all()
    return items


@router_5.get("/{item_id}", response_model=GradeResponse)
def get_grade(item_id: int, session: Session = Depends(get_session)):
    """Get a specific Grade by ID."""
    item = session.query(Grade).filter(Grade.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Grade not found")
    return item


@router_5.post("/", response_model=GradeResponse, status_code=status.HTTP_201_CREATED)
def create_grade(data: GradeCreate, session: Session = Depends(get_session)):
    """Create a new Grade."""
    # LLM_FILL: Apply business rule: A grade can only be assigned to an existing enrollment. One enrollment can have at most one grade.
    # Check that enrollment exists
    enrollment = session.query(Enrollment).filter(Enrollment.id == data.enrollment_id).first()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")

    # Check that this enrollment does not already have a grade (one-to-one constraint)
    existing_grade = session.query(Grade).filter(Grade.enrollment_id == data.enrollment_id).first()
    if existing_grade:
        raise HTTPException(status_code=409, detail="This enrollment already has a grade assigned")

    # LLM_FILL: Validate create_grade logic
    item = Grade(**data.model_dump())
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@router_5.put("/{item_id}", response_model=GradeResponse)
def update_grade(item_id: int, data: GradeUpdate, session: Session = Depends(get_session)):
    """Update an existing Grade."""
    item = session.query(Grade).filter(Grade.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Grade not found")
    # LLM_FILL: Validate update_grade logic
    # No additional business rules for grade updates (changing score is allowed)
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(item, key, value)
    session.commit()
    session.refresh(item)
    return item


@router_5.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_grade(item_id: int, session: Session = Depends(get_session)):
    """Delete a Grade."""
    item = session.query(Grade).filter(Grade.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Grade not found")
    # LLM_FILL: Validate delete_grade logic (cascade checks)
    # No dependent entities, safe to delete
    session.delete(item)
    session.commit()


router_6 = APIRouter(prefix="/assignments", tags=["Assignment"])


@router_6.get("/", response_model=List[AssignmentResponse])
def list_assignments(session: Session = Depends(get_session)):
    """List all assignments."""
    items = session.query(Assignment).all()
    return items


@router_6.get("/{item_id}", response_model=AssignmentResponse)
def get_assignment(item_id: int, session: Session = Depends(get_session)):
    """Get a specific Assignment by ID."""
    item = session.query(Assignment).filter(Assignment.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return item


@router_6.post("/", response_model=AssignmentResponse, status_code=status.HTTP_201_CREATED)
def create_assignment(data: AssignmentCreate, session: Session = Depends(get_session)):
    """Create a new Assignment."""
    # LLM_FILL: Apply business rule: Assignments submitted after the due date should be marked as late.
    # This rule requires a submission model which is not part of the current schema.
    # Without a submission entity, late marking cannot be implemented here.
    # As a placeholder, we note that when a submission feature is added, the submission time should be compared with due_date.

    # LLM_FILL: Validate create_assignment logic
    item = Assignment(**data.model_dump())
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@router_6.put("/{item_id}", response_model=AssignmentResponse)
def update_assignment(item_id: int, data: AssignmentUpdate, session: Session = Depends(get_session)):
    """Update an existing Assignment."""
    item = session.query(Assignment).filter(Assignment.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Assignment not found")
    # LLM_FILL: Validate update_assignment logic
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(item, key, value)
    session.commit()
    session.refresh(item)
    return item


@router_6.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_assignment(item_id: int, session: Session = Depends(get_session)):
    """Delete a Assignment."""
    item = session.query(Assignment).filter(Assignment.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Assignment not found")
    # LLM_FILL: Validate delete_assignment logic (cascade checks)
    # No dependent entities, safe to delete
    session.delete(item)
    session.commit()


# Collect all routers
routers = [
    router_1,
    router_2,
    router_3,
    router_4,
    router_5,
    router_6,
]