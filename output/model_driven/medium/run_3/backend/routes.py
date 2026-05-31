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
    # This rule is enforced at enrollment / course instructor assignment, not at user creation.
    # Validate create_user logic: ensure no duplicate username or email.
    if session.query(User).filter(User.username == data.username).first():
        raise HTTPException(status_code=409, detail="Username already exists")
    if session.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=409, detail="Email already exists")
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
    # LLM_FILL: Validate update_user logic: check uniqueness for username/email excluding self.
    if data.username is not None and data.username != item.username:
        if session.query(User).filter(User.username == data.username, User.id != item_id).first():
            raise HTTPException(status_code=409, detail="Username already taken")
    if data.email is not None and data.email != item.email:
        if session.query(User).filter(User.email == data.email, User.id != item_id).first():
            raise HTTPException(status_code=409, detail="Email already taken")
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
    # LLM_FILL: Validate delete_user logic (cascade checks): prevent deletion if user has dependents
    # (enrollments as student or courses as instructor)
    if session.query(Enrollment).filter(Enrollment.student_id == item_id).first():
        raise HTTPException(status_code=409, detail="Cannot delete user with existing enrollments")
    if session.query(Course).filter(Course.user_id == item_id).first():  # assuming instructor FK is user_id
        raise HTTPException(status_code=409, detail="Cannot delete user who is instructor of a course")
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
    # LLM_FILL: Validate create_department logic: check unique name and code.
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
    # LLM_FILL: Validate update_department logic: name/code uniqueness excluding self.
    if data.name is not None and data.name != item.name:
        if session.query(Department).filter(Department.name == data.name, Department.id != item_id).first():
            raise HTTPException(status_code=409, detail="Department name already taken")
    if data.code is not None and data.code != item.code:
        if session.query(Department).filter(Department.code == data.code, Department.id != item_id).first():
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
    # LLM_FILL: Validate delete_department logic (cascade checks): prevent deletion if courses exist.
    if session.query(Course).filter(Course.department_id == item_id).first():
        raise HTTPException(status_code=409, detail="Cannot delete department with existing courses")
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
    # (Not applicable here; enrollments are separate. Validating course creation below.)
    # LLM_FILL: Apply business rule: Prevent enrollment when the course has reached its maximum capacity.
    # (Enforced at enrollment creation, not course creation.)
    # LLM_FILL: Apply business rule: Prevent a student from enrolling in the same course more than once.
    # (Enforced at enrollment creation.)
    # LLM_FILL: Apply business rule: Only users with role 'student' can enroll in courses. Only users with role 'teacher' can be...
    # (Enforced at enrollment and instructor assignment.)
    # LLM_FILL: Apply business rule: A student cannot enroll in courses totaling more than 30 credits per semester.
    # (Enforced at enrollment creation.)
    # LLM_FILL: Validate create_course logic: ensure department exists, capacity/credits positive, no duplicate title per department.
    if not session.query(Department).filter(Department.id == data.department_id).first():
        raise HTTPException(status_code=404, detail="Department not found")
    if data.capacity <= 0:
        raise HTTPException(status_code=400, detail="Capacity must be positive")
    if data.credits <= 0:
        raise HTTPException(status_code=400, detail="Credits must be positive")
    # Optional: prevent duplicate title within the same department
    if session.query(Course).filter(
        Course.title == data.title, Course.department_id == data.department_id
    ).first():
        raise HTTPException(status_code=409, detail="A course with this title already exists in the department")
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
    # LLM_FILL: Validate update_course logic: ensure department exists if changed, non‑negative constraints, uniqueness.
    if data.department_id is not None:
        if not session.query(Department).filter(Department.id == data.department_id).first():
            raise HTTPException(status_code=404, detail="Department not found")
    if data.capacity is not None and data.capacity <= 0:
        raise HTTPException(status_code=400, detail="Capacity must be positive")
    if data.credits is not None and data.credits <= 0:
        raise HTTPException(status_code=400, detail="Credits must be positive")
    if data.title is not None and data.title != item.title:
        if session.query(Course).filter(
            Course.title == data.title,
            Course.department_id == (data.department_id if data.department_id is not None else item.department_id),
            Course.id != item_id
        ).first():
            raise HTTPException(status_code=409, detail="A course with this title already exists in the department")
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
    # LLM_FILL: Validate delete_course logic (cascade checks): cannot delete if enrollments or assignments exist.
    if session.query(Enrollment).filter(Enrollment.course_id == item_id).first():
        raise HTTPException(status_code=409, detail="Cannot delete course with existing enrollments")
    if session.query(Assignment).filter(Assignment.course_id == item_id).first():
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
    # LLM_FILL: Apply business rule: A grade can only be assigned to an existing enrollment. One enrollment can have at most one grade.
    # (Grade rule applies to grade creation, not here.)
    # LLM_FILL: Validate create_enrollment logic:
    #   1. Student role check, 2. Course existence & capacity, 3. Duplicate, 4. Credit limit
    
    # Ensure student exists and has role 'student'
    student = session.query(User).filter(User.id == data.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    if student.role != "student":
        raise HTTPException(status_code=400, detail="Only students can enroll in courses")
    
    # Ensure course exists
    course = session.query(Course).filter(Course.id == data.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Capacity check
    current_enrollments = session.query(Enrollment).filter(Enrollment.course_id == data.course_id).count()
    if current_enrollments >= course.capacity:
        raise HTTPException(status_code=409, detail="Course has reached its maximum capacity")
    
    # Duplicate enrollment check
    if session.query(Enrollment).filter(
        Enrollment.student_id == data.student_id,
        Enrollment.course_id == data.course_id
    ).first():
        raise HTTPException(status_code=409, detail="Student is already enrolled in this course")
    
    # Credit limit check: sum credits of all courses the student is enrolled in + new course
    total_credits = (
        session.query(Course.credits)
        .join(Enrollment, Enrollment.course_id == Course.id)
        .filter(Enrollment.student_id == data.student_id)
        .all()
    )
    current_credit_sum = sum(credit for (credit,) in total_credits)
    if current_credit_sum + course.credits > 30:
        raise HTTPException(status_code=400, detail="Enrollment would exceed the 30-credit limit")
    
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
    # LLM_FILL: Validate update_enrollment logic: enforce all creation rules if student or course changed.
    new_student_id = data.student_id if data.student_id is not None else item.student_id
    new_course_id = data.course_id if data.course_id is not None else item.course_id

    # If student changes, check role
    if new_student_id != item.student_id:
        student = session.query(User).filter(User.id == new_student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        if student.role != "student":
            raise HTTPException(status_code=400, detail="Only students can enroll in courses")
    
    # If course changes, check existence and capacity
    if new_course_id != item.course_id:
        course = session.query(Course).filter(Course.id == new_course_id).first()
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
        current_enrollments = session.query(Enrollment).filter(Enrollment.course_id == new_course_id).count()
        # When updating, exclude the current enrollment from capacity check
        if current_enrollments >= course.capacity:
            raise HTTPException(status_code=409, detail="Target course has reached its maximum capacity")
    
    # Duplicate check if student or course changed
    if new_student_id != item.student_id or new_course_id != item.course_id:
        duplicate = session.query(Enrollment).filter(
            Enrollment.student_id == new_student_id,
            Enrollment.course_id == new_course_id,
            Enrollment.id != item_id
        ).first()
        if duplicate:
            raise HTTPException(status_code=409, detail="Student is already enrolled in this course")
    
    # Credit limit check (if course changed and credits differ)
    if new_course_id != item.course_id or new_student_id != item.student_id:
        new_course = session.query(Course).filter(Course.id == new_course_id).first()
        # Get current total credits for the (potentially new) student excluding this enrollment
        total_credits = (
            session.query(Course.credits)
            .join(Enrollment, Enrollment.course_id == Course.id)
            .filter(Enrollment.student_id == new_student_id, Enrollment.id != item_id)
            .all()
        )
        current_sum = sum(credit for (credit,) in total_credits)
        if current_sum + new_course.credits > 30:
            raise HTTPException(status_code=400, detail="Enrollment would exceed the 30-credit limit")
    
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
    # LLM_FILL: Validate delete_enrollment logic (cascade checks): cannot delete if a grade exists.
    if session.query(Grade).filter(Grade.enrollment_id == item_id).first():
        raise HTTPException(status_code=409, detail="Cannot delete enrollment with an assigned grade")
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
    # LLM_FILL: Validate create_grade logic: check enrollment existence and uniqueness.
    enrollment = session.query(Enrollment).filter(Enrollment.id == data.enrollment_id).first()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    if session.query(Grade).filter(Grade.enrollment_id == data.enrollment_id).first():
        raise HTTPException(status_code=409, detail="An enrollment can have only one grade")
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
    # LLM_FILL: Validate update_grade logic: if enrollment changes, ensure new enrollment exists and no grade conflict.
    new_enrollment_id = data.enrollment_id if data.enrollment_id is not None else item.enrollment_id
    if new_enrollment_id != item.enrollment_id:
        enrollment = session.query(Enrollment).filter(Enrollment.id == new_enrollment_id).first()
        if not enrollment:
            raise HTTPException(status_code=404, detail="Enrollment not found")
        if session.query(Grade).filter(Grade.enrollment_id == new_enrollment_id, Grade.id != item_id).first():
            raise HTTPException(status_code=409, detail="Target enrollment already has a grade")
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
    # LLM_FILL: Validate delete_grade logic (cascade checks): no extra checks needed.
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
    # This rule pertains to submissions, not assignment creation. No submission entity exists,
    # so this rule is noted but not enforceable here.
    # LLM_FILL: Validate create