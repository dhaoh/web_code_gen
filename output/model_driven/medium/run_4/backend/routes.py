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
    allowed_roles = {"student", "teacher", "admin"}
    if data.role not in allowed_roles:
        raise HTTPException(status_code=400, detail=f"Role must be one of {allowed_roles}")
    
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
    if data.username and data.username != item.username:
        existing = session.query(User).filter(User.username == data.username).first()
        if existing:
            raise HTTPException(status_code=409, detail="Username already taken")
    if data.email and data.email != item.email:
        existing = session.query(User).filter(User.email == data.email).first()
        if existing:
            raise HTTPException(status_code=409, detail="Email already in use")
    if data.role and data.role not in {"student", "teacher", "admin"}:
        raise HTTPException(status_code=400, detail="Invalid role")

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
    # Prevent deletion if user has dependencies
    if item.role == "teacher":
        if session.query(Course).filter(Course.instructor_id == item_id).count() > 0:
            raise HTTPException(status_code=400, detail="Cannot delete teacher assigned to courses")
    if item.role == "student":
        if session.query(Enrollment).filter(Enrollment.student_id == item_id).count() > 0:
            raise HTTPException(status_code=400, detail="Cannot delete student with existing enrollments")
    # admin users might also be assigned as instructor? assume not, but handle generally
    if session.query(Enrollment).filter(Enrollment.student_id == item_id).count() > 0:
        raise HTTPException(status_code=400, detail="User has enrollments and cannot be deleted")
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
    existing = session.query(Department).filter(
        (Department.name == data.name) | (Department.code == data.code)
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail="Department with same name or code already exists")

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
    if data.name and data.name != item.name:
        if session.query(Department).filter(Department.name == data.name).count() > 0:
            raise HTTPException(status_code=409, detail="Department name already in use")
    if data.code and data.code != item.code:
        if session.query(Department).filter(Department.code == data.code).count() > 0:
            raise HTTPException(status_code=409, detail="Department code already in use")

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
    # LLM_FILL: Apply business rule: Prevent enrollment when the course has reached its maximum capacity.
    # LLM_FILL: Apply business rule: Prevent a student from enrolling in the same course more than once.
    # LLM_FILL: Apply business rule: Only users with role 'student' can enroll in courses. Only users with role 'teacher' can be...
    # LLM_FILL: Apply business rule: A student cannot enroll in courses totaling more than 30 credits per semester.
    # LLM_FILL: Validate create_course logic
    # Validate instructor is a teacher
    instructor = session.query(User).filter(User.id == data.instructor_id).first()
    if not instructor or instructor.role != "teacher":
        raise HTTPException(status_code=400, detail="Course instructor must be a teacher")
    # Check department exists
    department = session.query(Department).filter(Department.id == data.department_id).first()
    if not department:
        raise HTTPException(status_code=400, detail="Department not found")
    # Basic field checks
    if data.capacity <= 0:
        raise HTTPException(status_code=400, detail="Capacity must be positive")
    if data.credits <= 0:
        raise HTTPException(status_code=400, detail="Credits must be positive")

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
    # Validate instructor if changed
    if data.instructor_id and data.instructor_id != item.instructor_id:
        instructor = session.query(User).filter(User.id == data.instructor_id).first()
        if not instructor or instructor.role != "teacher":
            raise HTTPException(status_code=400, detail="Course instructor must be a teacher")
    # Validate department if changed
    if data.department_id and data.department_id != item.department_id:
        department = session.query(Department).filter(Department.id == data.department_id).first()
        if not department:
            raise HTTPException(status_code=400, detail="Department not found")
    # Validate fields
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
    # LLM_FILL: Validate delete_course logic (cascade checks)
    if session.query(Enrollment).filter(Enrollment.course_id == item_id).count() > 0:
        raise HTTPException(status_code=400, detail="Cannot delete course with existing enrollments")
    if session.query(Assignment).filter(Assignment.course_id == item_id).count() > 0:
        raise HTTPException(status_code=400, detail="Cannot delete course with existing assignments")
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
    # LLM_FILL: Apply business rule: A grade can only be assigned to an existing enrollment. One enrollment can have at most one grade.
    # LLM_FILL: Validate create_enrollment logic

    # 1. student role check
    student = session.query(User).filter(User.id == data.student_id).first()
    if not student or student.role != "student":
        raise HTTPException(status_code=400, detail="Only students can enroll in courses")

    # 2. course existence and capacity
    course = session.query(Course).filter(Course.id == data.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    current_enrollments = session.query(Enrollment).filter(Enrollment.course_id == data.course_id).count()
    if current_enrollments >= course.capacity:
        raise HTTPException(status_code=409, detail="Course has reached maximum capacity")

    # 3. duplicate enrollment
    existing_enrollment = session.query(Enrollment).filter(
        Enrollment.student_id == data.student_id,
        Enrollment.course_id == data.course_id
    ).first()
    if existing_enrollment:
        raise HTTPException(status_code=409, detail="Student is already enrolled in this course")

    # 4. credit limit (30 credits total across all enrollments)
    # Sum credits from all courses where the student is enrolled
    total_credits = session.query(Enrollment).filter(Enrollment.student_id == data.student_id).join(Course).count()  # Not correct: need sum of credits
    # Recalculate: sum credits of courses where student is enrolled
    credits_taken = session.query(Course.credits).join(Enrollment).filter(Enrollment.student_id == data.student_id).all()
    total_credits = sum(c[0] for c in credits_taken) if credits_taken else 0
    if total_credits + course.credits > 30:
        raise HTTPException(status_code=400, detail="Enrolling would exceed the 30-credit limit")

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
    # If student or course is changing, re-validate rules
    new_student_id = data.student_id if data.student_id else item.student_id
    new_course_id = data.course_id if data.course_id else item.course_id

    # check student role
    student = session.query(User).filter(User.id == new_student_id).first()
    if not student or student.role != "student":
        raise HTTPException(status_code=400, detail="Only students can enroll in courses")

    # check duplicate if changing pair
    if data.student_id or data.course_id:
        existing = session.query(Enrollment).filter(
            Enrollment.student_id == new_student_id,
            Enrollment.course_id == new_course_id,
            Enrollment.id != item_id
        ).first()
        if existing:
            raise HTTPException(status_code=409, detail="Student is already enrolled in this course")

    # check capacity if course changed
    if data.course_id and data.course_id != item.course_id:
        course = session.query(Course).filter(Course.id == new_course_id).first()
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
        current_enrollments = session.query(Enrollment).filter(Enrollment.course_id == new_course_id, Enrollment.id != item_id).count()
        if current_enrollments >= course.capacity:
            raise HTTPException(status_code=409, detail="Course has reached maximum capacity")

    # credit limit check (recalculate total credits excluding current enrollment, then add new course credits)
    if data.course_id or data.student_id:
        # Get all courses the student is enrolled in, excluding current enrollment
        enrolled_courses = session.query(Enrollment).filter(
            Enrollment.student_id == new_student_id,
            Enrollment.id != item_id
        ).all()
        total_credits = sum(e.course.credits for e in enrolled_courses if e.course)
        new_course = session.query(Course).filter(Course.id == new_course_id).first()
        if new_course and total_credits + new_course.credits > 30:
            raise HTTPException(status_code=400, detail="Enrollment change would exceed the 30-credit limit")

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
    # No specific rule prevents deletion, but we can allow it; related grades?
    # (optional) could prevent deletion if a grade exists? Not required by rules.
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
    # LLM_FILL: Validate create_grade logic

    # Check enrollment exists
    enrollment = session.query(Enrollment).filter(Enrollment.id == data.enrollment_id).first()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")

    # Check grade uniqueness per enrollment
    existing_grade = session.query(Grade).filter(Grade.enrollment_id == data.enrollment_id).first()
    if existing_grade:
        raise HTTPException(status_code=409, detail="This enrollment already has a grade")

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
    if data.enrollment_id and data.enrollment_id != item.enrollment_id:
        # validate new enrollment
        enrollment = session.query(Enrollment).filter(Enrollment.id == data.enrollment_id).first()
        if not enrollment:
            raise HTTPException(status_code=404, detail="Enrollment not found")
        # check uniqueness
        existing = session.query(Grade).filter(
            Grade.enrollment_id == data.enrollment_id,
            Grade.id != item_id
        ).first()
        if existing:
            raise HTTPException(status_code=409, detail="New enrollment already has a grade")

    for key, value in data.model_dump(exclude_unset=True).items():
        set