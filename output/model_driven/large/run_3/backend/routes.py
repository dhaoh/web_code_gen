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
    # LLM_FILL: Validate create_user logic
    # Check username uniqueness
    if session.query(User).filter(User.username == data.username).first():
        raise HTTPException(status_code=409, detail="Username already exists")
    # Check email uniqueness
    if session.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=409, detail="Email already exists")
    # Basic role validation
    if data.role not in ("student", "teacher", "admin", "department_head"):
        raise HTTPException(status_code=422, detail="Invalid role")
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
    # If username is being changed, ensure uniqueness
    if data.username and data.username != item.username:
        if session.query(User).filter(User.username == data.username).first():
            raise HTTPException(status_code=409, detail="Username already exists")
    # If email is being changed, ensure uniqueness
    if data.email and data.email != item.email:
        if session.query(User).filter(User.email == data.email).first():
            raise HTTPException(status_code=409, detail="Email already exists")
    if data.role and data.role not in ("student", "teacher", "admin", "department_head"):
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
    # Block if user is head of any department
    if session.query(Department).filter(Department.head_user_id == item_id).first():
        raise HTTPException(status_code=400, detail="Cannot delete user: user is department head")
    # Block if user teaches any course
    if session.query(Course).filter(Course.teacher_id == item_id).first():
        raise HTTPException(status_code=400, detail="Cannot delete user: user is assigned as teacher to courses")
    # Block if user has enrollments
    if session.query(Enrollment).filter(Enrollment.student_id == item_id).first():
        raise HTTPException(status_code=400, detail="Cannot delete user: user has enrollments")
    # Block if user has grades assigned as graded_by
    if session.query(Grade).filter(Grade.graded_by == item_id).first():
        raise HTTPException(status_code=400, detail="Cannot delete user: user has recorded grades")
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
    # LLM_FILL: Apply business rule: Only students can enroll in courses. Only teachers can be assigned as instructors. Only...
    # This business rule is enforced in enrollment / course creation endpoints.
    # LLM_FILL: Validate create_department logic
    # Check unique name and code
    if session.query(Department).filter(Department.name == data.name).first():
        raise HTTPException(status_code=409, detail="Department name already exists")
    if session.query(Department).filter(Department.code == data.code).first():
        raise HTTPException(status_code=409, detail="Department code already exists")
    # Validate head user if provided
    if data.head_user_id:
        head = session.query(User).filter(User.id == data.head_user_id).first()
        if not head:
            raise HTTPException(status_code=400, detail="Head user not found")
        # Department head should have appropriate role (optional: require department_head or teacher)
        if head.role not in ("department_head", "teacher", "admin"):
            raise HTTPException(status_code=400, detail="User must have a department_head or teacher role")
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
    # Check unique constraints if changing
    if data.name and data.name != item.name:
        if session.query(Department).filter(Department.name == data.name).first():
            raise HTTPException(status_code=409, detail="Department name already exists")
    if data.code and data.code != item.code:
        if session.query(Department).filter(Department.code == data.code).first():
            raise HTTPException(status_code=409, detail="Department code already exists")
    if data.head_user_id is not None and data.head_user_id != item.head_user_id:
        head = session.query(User).filter(User.id == data.head_user_id).first()
        if not head:
            raise HTTPException(status_code=400, detail="Head user not found")
        if head.role not in ("department_head", "teacher", "admin"):
            raise HTTPException(status_code=400, detail="User must have a department_head or teacher role")
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
    # Block if department has courses
    if session.query(Course).filter(Course.department_id == item_id).first():
        raise HTTPException(status_code=400, detail="Cannot delete department: it has associated courses")
    # Block if department has majors
    if session.query(Major).filter(Major.department_id == item_id).first():
        raise HTTPException(status_code=400, detail="Cannot delete department: it has associated majors")
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
    # LLM_FILL: Apply business rule: Students must complete all courses required by their major program. The system should track...
    # Tracking progress is a separate feature; here we just ensure basic integrity.
    # LLM_FILL: Validate create_major logic
    # Check unique code
    if session.query(Major).filter(Major.code == data.code).first():
        raise HTTPException(status_code=409, detail="Major code already exists")
    # Validate department
    dept = session.query(Department).filter(Department.id == data.department_id).first()
    if not dept:
        raise HTTPException(status_code=400, detail="Department not found")
    # Total credits must be positive
    if data.total_credits_required <= 0:
        raise HTTPException(status_code=422, detail="Total credits required must be positive")
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
    # LLM_FILL: Validate update_major logic
    if data.code and data.code != item.code:
        if session.query(Major).filter(Major.code == data.code).first():
            raise HTTPException(status_code=409, detail="Major code already exists")
    if data.department_id and data.department_id != item.department_id:
        dept = session.query(Department).filter(Department.id == data.department_id).first()
        if not dept:
            raise HTTPException(status_code=400, detail="Department not found")
    if data.total_credits_required is not None and data.total_credits_required <= 0:
        raise HTTPException(status_code=422, detail="Total credits required must be positive")
    for key, value in data.model_dump(exclude_unset=True).items():
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
    # LLM_FILL: Validate delete_major logic (cascade checks)
    # Block if any users are assigned to this major
    if session.query(User).filter(User.major_id == item_id).first():
        raise HTTPException(status_code=400, detail="Cannot delete major: there are users associated with it")
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
    # LLM_FILL: Check for existing Enrollment with same keys (duplicate check)
    # This check belongs to enrollment creation; not relevant here.
    # LLM_FILL: Check for existing CourseSchedule with same keys (duplicate check)
    # Not relevant here.
    # LLM_FILL: Apply business rule: Prevent enrollment when course has reached maximum capacity.
    # This is enforced during enrollment creation.
    # LLM_FILL: Apply business rule: Prevent a student from enrolling in the same course twice.
    # Enforced during enrollment creation.
    # LLM_FILL: Apply business rule: Only students can enroll in courses. Only teachers can be assigned as instructors. Only...
    # Enforce teacher assignment rule here.
    # LLM_FILL: Apply business rule: A student must have completed all mandatory prerequisites before enrolling in a course....
    # Enforced during enrollment creation.
    # LLM_FILL: Apply business rule: A student cannot enroll in courses that have overlapping schedules.
    # Enforced during enrollment creation.

    # LLM_FILL: Apply business rule: A student cannot enroll in courses totaling more than 30 credits per semester.
    # Enforced during enrollment creation.

    # LLM_FILL: Apply business rule: A grade can only be assigned to an existing enrollment. One enrollment gets at most one grade....
    # Enforced during grade creation.

    # LLM_FILL: Apply business rule: Course enrollment cannot exceed the assigned classroom capacity.
    # Enforced during enrollment creation.

    # LLM_FILL: Apply business rule: Students must complete all courses required by their major program. The system should track...
    # Tracking not needed at course creation.

    # LLM_FILL: Validate create_course logic
    # Check unique code
    if session.query(Course).filter(Course.code == data.code).first():
        raise HTTPException(status_code=409, detail="Course code already exists")
    # Validate department
    dept = session.query(Department).filter(Department.id == data.department_id).first()
    if not dept:
        raise HTTPException(status_code=400, detail="Department not found")
    # Validate teacher exists and has teacher role
    teacher = session.query(User).filter(User.id == data.teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=400, detail="Teacher not found")
    if teacher.role != "teacher":
        raise HTTPException(status_code=400, detail="Assigned instructor must have teacher role")
    # If classroom provided, validate it
    if data.classroom_id:
        classroom = session.query(Classroom).filter(Classroom.id == data.classroom_id).first()
        if not classroom:
            raise HTTPException(status_code=400, detail="Classroom not found")
        # Optionally check that capacity matches? Not strictly required but could warn if classroom capacity < course capacity.
        if data.capacity > classroom.capacity:
            raise HTTPException(status_code=400, detail="Course capacity cannot exceed classroom capacity")
    # Credits and capacity must be positive
    if data.credits <= 0:
        raise HTTPException(status_code=422, detail="Credits must be positive")
    if data.capacity <= 0:
        raise HTTPException(status_code=422, detail="Capacity must be positive")
    item = Course(**data.model_dump())
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@router_4.put("/{item_id}", response_model=CourseResponse)
def update_course(item_id: int, data: CourseUpdate, session: Session = Depends(get_session)):
    """Update an existing Course."""
    item = session.query(Course).filter(Course.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Course not found")
    # LLM_FILL: Validate update_course logic
    if data.code and data.code != item.code:
        if session.query(Course).filter(Course.code == data.code).first():
            raise HTTPException(status_code=409, detail="Course code already exists")
    if data.department_id and data.department_id != item.department_id:
        dept = session.query(Department).filter(Department.id == data.department_id).first()
        if not dept:
            raise HTTPException(status_code=400, detail="Department not found")
    if data.teacher_id is not None and data.teacher_id != item.teacher_id:
        teacher = session.query(User).filter(User.id == data.teacher_id).first()
        if not teacher:
            raise HTTPException(status_code=400, detail="Teacher not found")
        if teacher.role != "teacher":
            raise HTTPException(status_code=400, detail="Assigned instructor must have teacher role")
    # If classroom changes, validate and check capacity
    if data.classroom_id is not None and data.classroom_id != item.classroom_id:
        classroom = session.query(Classroom).filter(Classroom.id == data.classroom_id).first()
        if not classroom:
            raise HTTPException(status_code=400, detail="Classroom not found")
        # Determine effective capacity: updated capacity or current
        effective_capacity = data.capacity if data.capacity is not None else item.capacity
        if effective_capacity > classroom.capacity:
            raise HTTPException(status_code=400, detail="Course capacity cannot exceed classroom capacity")
    # If capacity is changed without classroom change, still check the existing classroom
    if data.capacity is not None and data.capacity != item.capacity:
        if item.classroom_id:
            classroom = session.query(Classroom).filter(Classroom.id == item.classroom_id).first()
            if classroom and data.capacity > classroom.capacity:
                raise HTTPException(status_code=400, detail="Course capacity cannot exceed classroom capacity")
        if data.capacity <= 0:
            raise HTTPException(status_code=422, detail="Capacity must be positive")
    if data.credits is not None and data.credits <= 0:
        raise HTTPException(status_code=422, detail="Credits must be positive")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(item, key, value)
    session.commit()
    session.refresh(item)
    return item


@router_4.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(item_id: int, session: Session = Depends(get_session)):
    """Delete a Course."""
    item = session.query(Course).filter(Course.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Course not found")
    # LLM_FILL: Validate delete_course logic (cascade checks)
    # Block if course has enrollments
    if session.query(Enrollment).filter(Enrollment.course_id == item_id).first():
        raise HTTPException(status_code=400, detail="Cannot delete course: it has enrollments")
    # Block if course has prerequisites (as course_id) or is a prerequisite (prerequisite_course_id)
    if session.query(Prerequisite).filter((Prerequisite.course_id == item_id) | (Prerequisite.prerequisite_course_id == item_id)).first():
        raise HTTPException(status_code=400, detail="Cannot delete course: it has prerequisites")
    # Block if course has schedules
    if session.query(CourseSchedule).filter(CourseSchedule.course_id == item_id).first():
        raise HTTPException(status_code=400, detail="Cannot delete course: it has schedules")
    # Block if course has assignments
    if session.query(Assignment).filter(Assignment.course_id == item_id).first():
        raise HTTPException(status_code=400, detail="Cannot delete course: it has assignments")
    session.delete(item)
    session.commit()


router_5 = APIRouter(prefix="/prerequisites", tags=["Prerequisite"])


@router_5.get("/", response_model=List[PrerequisiteResponse])
def list_prerequisites(session: Session = Depends(get_session)):
    """List all prerequisites."""
    items = session.query(Prerequisite).all()
    return items


@router_5.get("/{item_id}", response_model=PrerequisiteResponse)
def get_prerequisite(item_id: int, session: Session = Depends(get_session)):
    """Get a specific Prerequisite by ID."""
    item = session.query(Prerequisite).filter(Prerequisite.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Prerequisite not found")
    return item


@router_5.post("/", response_model=PrerequisiteResponse, status_code=status.HTTP_201_CREATED)
def create_prerequisite(data: PrerequisiteCreate, session: Session = Depends(get_session)):
    """Create a new Prerequisite."""
    # LLM_FILL: Validate create_prerequisite logic
    # Check that course and prerequisite_course exist
    course = session.query(Course).filter(Course.id == data.course_id).first()
    if not course:
        raise HTTPException(status_code=400, detail="Course not found")
    prereq_course = session.query(Course).filter(Course.id == data.prerequisite_course_id).first()
    if not prereq_course:
        raise HTTPException(status_code=400, detail="Prerequisite course not found")
    # Prevent self-referencing
    if data.course_id == data.prerequisite_course_id:
        raise HTTPException(status_code=400, detail="A course cannot be a prerequisite of itself")
    # Check for duplicate relationship (course_id, prerequisite_course_id) regardless of mandatory flag
    existing = session.query(Prerequisite).filter(
        Prerequisite.course_id == data.course_id,
        Prerequisite.prerequisite_course_id == data.prerequisite_course_id
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail="This prerequisite relationship already exists")
    item = Prerequisite(**data.model_dump())
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@router_5.put("/{item_id}", response_model=PrerequisiteResponse)
def update_prerequisite(item_id: int, data: PrerequisiteUpdate, session: Session = Depends(get_session)):
    """Update an existing Prerequisite."""
    item = session.query(Prerequisite).filter(Prerequisite.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Prerequisite not found")
    # LLM_FILL: Validate update_prerequisite logic
    # If changing course or prerequisite_course, validate existence
    new_course_id = data.course_id if data.course_id is not None else item.course_id
    new_prereq_course_id = data.prerequisite_course_id if data.prerequisite_course_id is not None else item.prerequisite_course_id
    if new_course_id != item.course_id or new_prereq_course_id != item.prerequisite_course_id:
        course = session.query(Course).filter(Course.id == new_course_id).first()
        if not course:
            raise HTTPException(status_code=400, detail="Course not found")
        prereq_course = session.query(Course).filter(Course.id == new_prereq_course_id).first()
        if not prereq_course:
            raise HTTPException(status_code=400, detail="Prerequisite course not found")
        if new_course_id == new_prereq_course_id:
            raise HTTPException(status_code=400, detail="A course cannot be a prerequisite of itself")
        # Check for duplicate relationship ignoring current item
        existing = session.query(Prerequisite).filter(
            Prerequisite.course_id == new_course_id,
            Prerequisite.prerequisite_course_id == new_prereq_course_id,
            Prerequisite.id != item_id
        ).first()
        if existing:
            raise HTTPException(status_code=409, detail="This prerequisite relationship already exists")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(item, key, value)
    session.commit()
    session.refresh(item)
    return item


@router_5.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_prerequisite(item_id: int, session: Session = Depends(get_session)):
    """Delete a Prerequisite."""
    item = session.query(Prerequisite).filter(Prerequisite.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Prerequisite not found")
    session.delete(item)
    session.commit()


router_6 = APIRouter(prefix="/classrooms", tags=["Classroom"])


@router_6.get("/", response_model=List[ClassroomResponse])
def list_classrooms(session: Session = Depends(get_session)):
    """List all classrooms."""
    items = session.query(Classroom).all()
    return items


@router_6.get("/{item_id}", response_model=ClassroomResponse)
def get_classroom(item_id: int, session: Session = Depends(get_session)):
    """Get a specific Classroom by ID."""
    item = session.query(Classroom).filter(Classroom.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Classroom not found")
    return item


@router_6.post("/", response_model=ClassroomResponse, status_code=status.HTTP_201_CREATED)
def create_classroom(data: ClassroomCreate, session: Session = Depends(get_session)):
    """Create a new Classroom."""
    # LLM_FILL: Validate create_classroom logic
    # Capacity must be positive
    if data.capacity <= 0:
        raise HTTPException(status_code=422, detail="Capacity must be positive")
    # optional: check for duplicate building+room_number? Not strictly required but could be nice.
    item = Classroom(**data.model_dump())
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@router_6.put("/{item_id}", response_model=ClassroomResponse)
def update_classroom(item_id: int, data: ClassroomUpdate, session: Session = Depends(get_session)):
    """Update an existing Classroom."""
    item = session.query(Classroom).filter(Classroom.id == item_id).first()
    if not item:
        raise HTTPException