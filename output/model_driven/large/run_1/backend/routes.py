"""API routes for student_course_system_large.
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
    allowed_roles = ["student", "teacher", "head_of_department"]
    if data.role not in allowed_roles:
        raise HTTPException(status_code=422, detail=f"Invalid role: {data.role}. Allowed: {allowed_roles}")
    existing = session.query(User).filter(User.username == data.username).first()
    if existing:
        raise HTTPException(status_code=409, detail="Username already exists")
    existing_email = session.query(User).filter(User.email == data.email).first()
    if existing_email:
        raise HTTPException(status_code=409, detail="Email already exists")
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
    # LLM_FILL: Validate update_user logic
    update_data = data.model_dump(exclude_unset=True)
    if "username" in update_data and update_data["username"] != item.username:
        existing = session.query(User).filter(User.username == update_data["username"]).first()
        if existing:
            raise HTTPException(status_code=409, detail="Username already exists")
    if "email" in update_data and update_data["email"] != item.email:
        existing_email = session.query(User).filter(User.email == update_data["email"]).first()
        if existing_email:
            raise HTTPException(status_code=409, detail="Email already exists")
    if "role" in update_data:
        allowed_roles = ["student", "teacher", "head_of_department"]
        if update_data["role"] not in allowed_roles:
            raise HTTPException(status_code=422, detail=f"Invalid role: {update_data['role']}")
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
    # LLM_FILL: Validate delete_user logic (cascade checks)
    # Check if user is referenced as teacher in any course
    taught_courses = session.query(Course).filter(Course.teacher_id == item_id).first()
    if taught_courses:
        raise HTTPException(status_code=409, detail="Cannot delete user: assigned as teacher to one or more courses")
    # Check if user is head of any department
    headed_department = session.query(Department).filter(Department.head_user_id == item_id).first()
    if headed_department:
        raise HTTPException(status_code=409, detail="Cannot delete user: assigned as head of department")
    # Check if user has enrollments as student
    student_enrollments = session.query(Enrollment).filter(Enrollment.student_id == item_id).first()
    if student_enrollments:
        raise HTTPException(status_code=409, detail="Cannot delete user: has one or more enrollments")
    # Check if user has graded any assignment
    graded = session.query(Grade).filter(Grade.graded_by == item_id).first()
    if graded:
        # Could set graded_by to null, but prefer to block
        raise HTTPException(status_code=409, detail="Cannot delete user: has graded one or more assignments")
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
    # (Authorization rule: not enforced here without request context)
    # LLM_FILL: Validate create_department logic
    existing = session.query(Department).filter(Department.code == data.code).first()
    if existing:
        raise HTTPException(status_code=409, detail="Department code already exists")
    if data.head_user_id is not None:
        head = session.query(User).filter(User.id == data.head_user_id).first()
        if not head:
            raise HTTPException(status_code=400, detail="Head user not found")
        if head.role not in ["head_of_department", "teacher"]:
            raise HTTPException(status_code=422, detail="Head user must have role head_of_department or teacher")
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
    update_data = data.model_dump(exclude_unset=True)
    if "code" in update_data and update_data["code"] != item.code:
        existing = session.query(Department).filter(Department.code == update_data["code"]).first()
        if existing:
            raise HTTPException(status_code=409, detail="Department code already exists")
    if "head_user_id" in update_data and update_data["head_user_id"] is not None:
        head = session.query(User).filter(User.id == update_data["head_user_id"]).first()
        if not head:
            raise HTTPException(status_code=400, detail="Head user not found")
        if head.role not in ["head_of_department", "teacher"]:
            raise HTTPException(status_code=422, detail="Head user must have role head_of_department or teacher")
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
    # LLM_FILL: Validate delete_department logic (cascade checks)
    courses = session.query(Course).filter(Course.department_id == item_id).first()
    if courses:
        raise HTTPException(status_code=409, detail="Cannot delete department: has associated courses")
    majors = session.query(Major).filter(Major.department_id == item_id).first()
    if majors:
        raise HTTPException(status_code=409, detail="Cannot delete department: has associated majors")
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
    # (Tracking is outside create scope; major creation just stores requirements.)
    # LLM_FILL: Validate create_major logic
    existing = session.query(Major).filter(Major.code == data.code).first()
    if existing:
        raise HTTPException(status_code=409, detail="Major code already exists")
    department = session.query(Department).filter(Department.id == data.department_id).first()
    if not department:
        raise HTTPException(status_code=400, detail="Department not found")
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
    update_data = data.model_dump(exclude_unset=True)
    if "code" in update_data and update_data["code"] != item.code:
        existing = session.query(Major).filter(Major.code == update_data["code"]).first()
        if existing:
            raise HTTPException(status_code=409, detail="Major code already exists")
    if "department_id" in update_data and update_data["department_id"] is not None:
        department = session.query(Department).filter(Department.id == update_data["department_id"]).first()
        if not department:
            raise HTTPException(status_code=400, detail="Department not found")
    if "total_credits_required" in update_data and update_data["total_credits_required"] <= 0:
        raise HTTPException(status_code=422, detail="Total credits required must be positive")
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
    # LLM_FILL: Validate delete_major logic
    users = session.query(User).filter(User.major_id == item_id).first()
    if users:
        raise HTTPException(status_code=409, detail="Cannot delete major: has associated users")
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
    # LLM_FILL: Validate create_course logic
    existing = session.query(Course).filter(Course.code == data.code).first()
    if existing:
        raise HTTPException(status_code=409, detail="Course code already exists")
    department = session.query(Department).filter(Department.id == data.department_id).first()
    if not department:
        raise HTTPException(status_code=400, detail="Department not found")
    teacher = session.query(User).filter(User.id == data.teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=400, detail="Teacher not found")
    if teacher.role not in ["teacher", "head_of_department"]:
        raise HTTPException(status_code=422, detail="Instructor must be a teacher or head of department")
    if data.classroom_id is not None:
        classroom = session.query(Classroom).filter(Classroom.id == data.classroom_id).first()
        if not classroom:
            raise HTTPException(status_code=400, detail="Classroom not found")
    if data.capacity <= 0:
        raise HTTPException(status_code=422, detail="Course capacity must be positive")
    if data.credits <= 0:
        raise HTTPException(status_code=422, detail="Credits must be positive")
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
    update_data = data.model_dump(exclude_unset=True)
    if "code" in update_data and update_data["code"] != item.code:
        existing = session.query(Course).filter(Course.code == update_data["code"]).first()
        if existing:
            raise HTTPException(status_code=409, detail="Course code already exists")
    if "department_id" in update_data:
        dept = session.query(Department).filter(Department.id == update_data["department_id"]).first()
        if not dept:
            raise HTTPException(status_code=400, detail="Department not found")
    if "teacher_id" in update_data:
        teacher = session.query(User).filter(User.id == update_data["teacher_id"]).first()
        if not teacher:
            raise HTTPException(status_code=400, detail="Teacher not found")
        if teacher.role not in ["teacher", "head_of_department"]:
            raise HTTPException(status_code=422, detail="Instructor must be a teacher or head of department")
    if "classroom_id" in update_data and update_data["classroom_id"] is not None:
        classroom = session.query(Classroom).filter(Classroom.id == update_data["classroom_id"]).first()
        if not classroom:
            raise HTTPException(status_code=400, detail="Classroom not found")
    if "capacity" in update_data and update_data["capacity"] <= 0:
        raise HTTPException(status_code=422, detail="Course capacity must be positive")
    if "credits" in update_data and update_data["credits"] <= 0:
        raise HTTPException(status_code=422, detail="Credits must be positive")
    for key, value in update_data.items():
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
    # LLM_FILL: Validate delete_course logic
    enrollments = session.query(Enrollment).filter(Enrollment.course_id == item_id).first()
    if enrollments:
        raise HTTPException(status_code=409, detail="Cannot delete course: has enrollments")
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
    course = session.query(Course).filter(Course.id == data.course_id).first()
    if not course:
        raise HTTPException(status_code=400, detail="Course not found")
    prereq_course = session.query(Course).filter(Course.id == data.prerequisite_course_id).first()
    if not prereq_course:
        raise HTTPException(status_code=400, detail="Prerequisite course not found")
    if data.course_id == data.prerequisite_course_id:
        raise HTTPException(status_code=422, detail="A course cannot be a prerequisite of itself")
    existing = session.query(Prerequisite).filter(
        Prerequisite.course_id == data.course_id,
        Prerequisite.prerequisite_course_id == data.prerequisite_course_id
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail="Prerequisite already exists")
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
    update_data = data.model_dump(exclude_unset=True)
    if "course_id" in update_data or "prerequisite_course_id" in update_data:
        course_id = update_data.get("course_id", item.course_id)
        prereq_id = update_data.get("prerequisite_course_id", item.prerequisite_course_id)
        if course_id == prereq_id:
            raise HTTPException(status_code=422, detail="A course cannot be a prerequisite of itself")
    for key, value in update_data.items():
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
    if data.capacity <= 0:
        raise HTTPException(status_code=422, detail="Classroom capacity must be positive")
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
        raise HTTPException(status_code=404, detail="Classroom not found")
    update_data = data.model_dump(exclude_unset=True)
    if "capacity" in update_data and update_data["capacity"] <= 0:
        raise HTTPException(status_code=422, detail="Classroom capacity must be positive")
    for key, value in update_data.items():
        setattr(item, key, value)
    session.commit()
    session.refresh(item)
    return item


@router_6.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_classroom(item_id: int, session: Session = Depends(get_session)):
    """Delete a Classroom."""
    item = session.query(Classroom).filter(Classroom.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Classroom not found")
    # Check if any course uses this classroom
    course = session.query(Course).filter(Course.classroom_id == item_id).first()
    if course:
        raise HTTPException(status_code=409, detail="Cannot delete classroom: assigned to one or more courses")
    session.delete(item)
    session.commit()


router_7 = APIRouter(prefix="/schedules", tags=["Schedule"])


@router_7.get("/", response_model=List[ScheduleResponse])
def list_schedules(session: Session = Depends(get_session)):
    """List all schedules."""
    items = session.query(Schedule).all()
    return items


@router_7.get("/{item_id}", response_model=ScheduleResponse)
def get_schedule(item_id: int, session: Session = Depends(get_session)):
    """Get a specific Schedule by ID."""
    item = session.query(Schedule).filter(Schedule.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return item


@router_7.post("/", response_model=ScheduleResponse, status_code=status.HTTP_201_CREATED)
def create_schedule(data: ScheduleCreate, session: Session = Depends(get_session)):
    """Create a new Schedule."""
    if data.day_of_week < 1 or data.day_of_week > 7:
        raise HTTPException(status_code=422, detail="Day of week must be between 1 (Monday) and 7 (Sunday)")
    item = Schedule(**data.model_dump())
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@router_7.put("/{item_id}", response_model=ScheduleResponse)
def update_schedule(item_id: int, data: ScheduleUpdate, session: Session = Depends(get_session)):
    """Update an existing Schedule."""
    item = session.query(Schedule).filter(Schedule.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Schedule not found")
    update_data = data.model_dump(exclude_unset=True)
    if "day_of_week" in update_data and (update_data["day_of_week"] < 1 or update_data["day_of_week"] > 7):
        raise HTTPException(status_code=422, detail="Day of week must be between 1 and 7")
    for key, value in update_data.items():
        setattr(item, key, value)
    session.commit()
    session.refresh(item)
    return item


@router_7.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_schedule(item_id: int, session: Session = Depends(get_session)):
    """Delete a Schedule."""
    item = session.query(Schedule).filter(Schedule.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Schedule not found")
    # Check if any course uses this schedule