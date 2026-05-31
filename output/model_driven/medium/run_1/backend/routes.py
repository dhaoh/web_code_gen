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
    # LLM_FILL: Validate create_user logic
    # Validate role is allowed
    if data.role not in ('student', 'teacher', 'admin'):
        raise HTTPException(status_code=422, detail="Role must be 'student', 'teacher', or 'admin'")
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
    if data.role is not None and data.role not in ('student', 'teacher', 'admin'):
        raise HTTPException(status_code=422, detail="Role must be 'student', 'teacher', or 'admin'")
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
    # No specific business rule; cascade deletion handled by database relationships.
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
    # No specific business rule; cascade deletion handled by database.
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
    # Not applicable for course creation; duplicate enrollment is handled in enrollment creation.
    # LLM_FILL: Apply business rule: Prevent enrollment when the course has reached its maximum capacity.
    # Not applicable; capacity check is performed during enrollment creation.
    # LLM_FILL: Apply business rule: Prevent a student from enrolling in the same course more than once.
    # Not applicable; handled in enrollment creation.
    # LLM_FILL: Apply business rule: Only users with role 'student' can enroll in courses. Only users with role 'teacher' can be...
    # Ensure instructor (if provided) has teacher role
    if hasattr(data, 'instructor_id') and data.instructor_id is not None:
        instructor = session.query(User).filter(User.id == data.instructor_id).first()
        if not instructor:
            raise HTTPException(status_code=400, detail="Instructor not found")
        if instructor.role != 'teacher':
            raise HTTPException(status_code=400, detail="Course instructor must be a teacher")
    # LLM_FILL: Apply business rule: A student cannot enroll in courses totaling more than 30 credits per semester.
    # Not applicable; credit limit is enforced at enrollment time.
    # LLM_FILL: Validate create_course logic
    if data.capacity <= 0:
        raise HTTPException(status_code=400, detail="Capacity must be positive")
    if data.credits <= 0:
        raise HTTPException(status_code=400, detail="Credits must be positive")
    department = session.query(Department).filter(Department.id == data.department_id).first()
    if not department:
        raise HTTPException(status_code=400, detail="Department not found")
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
    # Validate instructor role if updated
    if data.instructor_id is not None:
        instructor = session.query(User).filter(User.id == data.instructor_id).first()
        if not instructor:
            raise HTTPException(status_code=400, detail="Instructor not found")
        if instructor.role != 'teacher':
            raise HTTPException(status_code=400, detail="Course instructor must be a teacher")
    if data.capacity is not None and data.capacity <= 0:
        raise HTTPException(status_code=400, detail="Capacity must be positive")
    if data.credits is not None and data.credits <= 0:
        raise HTTPException(status_code=400, detail="Credits must be positive")
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
    session.delete(item)
    session.commit()


router_4 = APIRouter(prefix="/enrollments", tags=["Enrollment"])


@router_4.get("/", response_model=List[EnrollmentResponse])
def list_enrollments(session: Session = Depends(get_session)):
    items = session.query(Enrollment).all()
    return items


@router_4.get("/{item_id}", response_model=EnrollmentResponse)
def get_enrollment(item_id: int, session: Session = Depends(get_session)):
    item = session.query(Enrollment).filter(Enrollment.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return item


@router_4.post("/", response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED)
def create_enrollment(data: EnrollmentCreate, session: Session = Depends(get_session)):
    """Enroll a student in a course, applying business rules."""
    # Student role check
    student = session.query(User).filter(User.id == data.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    if student.role != 'student':
        raise HTTPException(status_code=400, detail="Only students can enroll in courses")

    # Course existence
    course = session.query(Course).filter(Course.id == data.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # Duplicate enrollment check
    existing = session.query(Enrollment).filter(
        Enrollment.student_id == data.student_id,
        Enrollment.course_id == data.course_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Student is already enrolled in this course")

    # Capacity check
    enrolled_count = session.query(Enrollment).filter(
        Enrollment.course_id == data.course_id
    ).count()
    if enrolled_count >= course.capacity:
        raise HTTPException(status_code=400, detail="Course has reached maximum capacity")

    # Credit limit check
    total_credits = session.query(Course.credits).join(
        Enrollment, Enrollment.course_id == Course.id
    ).filter(Enrollment.student_id == data.student_id).all()
    current_credits = sum(c[0] for c in total_credits)
    if current_credits + course.credits > 30:
        raise HTTPException(status_code=400, detail="Enrolling in this course would exceed the 30-credit limit")

    enrollment = Enrollment(**data.model_dump())
    session.add(enrollment)
    session.commit()
    session.refresh(enrollment)
    return enrollment


@router_4.put("/{item_id}", response_model=EnrollmentResponse)
def update_enrollment(item_id: int, data: EnrollmentUpdate, session: Session = Depends(get_session)):
    """Update enrollment details."""
    enrollment = session.query(Enrollment).filter(Enrollment.id == item_id).first()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    # LLM_FILL: Apply appropriate business rules on update if needed
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(enrollment, key, value)
    session.commit()
    session.refresh(enrollment)
    return enrollment


@router_4.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_enrollment(item_id: int, session: Session = Depends(get_session)):
    enrollment = session.query(Enrollment).filter(Enrollment.id == item_id).first()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    session.delete(enrollment)
    session.commit()


router_5 = APIRouter(prefix="/grades", tags=["Grade"])


@router_5.get("/", response_model=List[GradeResponse])
def list_grades(session: Session = Depends(get_session)):
    return session.query(Grade).all()


@router_5.get("/{item_id}", response_model=GradeResponse)
def get_grade(item_id: int, session: Session = Depends(get_session)):
    grade = session.query(Grade).filter(Grade.id == item_id).first()
    if not grade:
        raise HTTPException(status_code=404, detail="Grade not found")
    return grade


@router_5.post("/", response_model=GradeResponse, status_code=status.HTTP_201_CREATED)
def create_grade(data: GradeCreate, session: Session = Depends(get_session)):
    """Create a grade for an enrollment."""
    enrollment = session.query(Enrollment).filter(Enrollment.id == data.enrollment_id).first()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")

    # Grade can only be assigned to existing enrollment (already checked)
    # One enrollment can have at most one grade
    existing_grade = session.query(Grade).filter(Grade.enrollment_id == data.enrollment_id).first()
    if existing_grade:
        raise HTTPException(status_code=400, detail="An enrollment can only have one grade")

    grade = Grade(**data.model_dump())
    session.add(grade)
    session.commit()
    session.refresh(grade)
    return grade


@router_5.put("/{item_id}", response_model=GradeResponse)
def update_grade(item_id: int, data: GradeUpdate, session: Session = Depends(get_session)):
    grade = session.query(Grade).filter(Grade.id == item_id).first()
    if not grade:
        raise HTTPException(status_code=404, detail="Grade not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(grade, key, value)
    session.commit()
    session.refresh(grade)
    return grade


@router_5.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_grade(item_id: int, session: Session = Depends(get_session)):
    grade = session.query(Grade).filter(Grade.id == item_id).first()
    if not grade:
        raise HTTPException(status_code=404, detail="Grade not found")
    session.delete(grade)
    session.commit()


router_6 = APIRouter(prefix="/assignments", tags=["Assignment"])


@router_6.get("/", response_model=List[AssignmentResponse])
def list_assignments(session: Session = Depends(get_session)):
    return session.query(Assignment).all()


@router_6.get("/{item_id}", response_model=AssignmentResponse)
def get_assignment(item_id: int, session: Session = Depends(get_session)):
    assignment = session.query(Assignment).filter(Assignment.id == item_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return assignment


@router_6.post("/", response_model=AssignmentResponse, status_code=status.HTTP_201_CREATED)
def create_assignment(data: AssignmentCreate, session: Session = Depends(get_session)):
    # Validate course exists
    course = session.query(Course).filter(Course.id == data.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    assignment = Assignment(**data.model_dump())
    session.add(assignment)
    session.commit()
    session.refresh(assignment)
    return assignment


@router_6.put("/{item_id}", response_model=AssignmentResponse)
def update_assignment(item_id: int, data: AssignmentUpdate, session: Session = Depends(get_session)):
    assignment = session.query(Assignment).filter(Assignment.id == item_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(assignment, key, value)
    session.commit()
    session.refresh(assignment)
    return assignment


@router_6.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_assignment(item_id: int, session: Session = Depends(get_session)):
    assignment = session.query(Assignment).filter(Assignment.id == item_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    session.delete(assignment)
    session.commit()