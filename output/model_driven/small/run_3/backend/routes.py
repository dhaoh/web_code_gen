"""
API routes for student_course_system_small.
Generated from model definition.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from models import (
    Student,
    Course,
    Enrollment,
    get_session,
)
from schemas import (
    StudentCreate,
    StudentUpdate,
    StudentResponse,
    CourseCreate,
    CourseUpdate,
    CourseResponse,
    EnrollmentCreate,
    EnrollmentUpdate,
    EnrollmentResponse,
)

router_1 = APIRouter(prefix="/students", tags=["Student"])


@router_1.get("/", response_model=List[StudentResponse])
def list_students(session: Session = Depends(get_session)):
    """List all students."""
    items = session.query(Student).all()
    return items


@router_1.get("/{item_id}", response_model=StudentResponse)
def get_student(item_id: int, session: Session = Depends(get_session)):
    """Get a specific Student by ID."""
    item = session.query(Student).filter(Student.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Student not found")
    return item


@router_1.post("/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(data: StudentCreate, session: Session = Depends(get_session)):
    """Create a new Student."""
    # LLM_FILL: Check for existing Enrollment with same keys (duplicate check)
    # LLM_FILL: Apply business rule: Prevent a student from enrolling in the same course more than once. The system must check for...
    # LLM_FILL: Validate create_student logic
    existing = session.query(Student).filter(Student.email == data.email).first()
    if existing:
        raise HTTPException(status_code=409, detail="A student with this email already exists")
    item = Student(**data.model_dump())
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@router_1.put("/{item_id}", response_model=StudentResponse)
def update_student(item_id: int, data: StudentUpdate, session: Session = Depends(get_session)):
    """Update an existing Student."""
    item = session.query(Student).filter(Student.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Student not found")
    # LLM_FILL: Validate update_student logic
    if data.email and data.email != item.email:
        conflict = session.query(Student).filter(Student.email == data.email, Student.id != item_id).first()
        if conflict:
            raise HTTPException(status_code=409, detail="A student with this email already exists")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(item, key, value)
    session.commit()
    session.refresh(item)
    return item


@router_1.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(item_id: int, session: Session = Depends(get_session)):
    """Delete a Student."""
    item = session.query(Student).filter(Student.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Student not found")
    # LLM_FILL: Validate delete_student logic (cascade checks)
    enrollments = session.query(Enrollment).filter(Enrollment.student_id == item_id).all()
    for enrollment in enrollments:
        session.delete(enrollment)
    session.delete(item)
    session.commit()


router_2 = APIRouter(prefix="/courses", tags=["Course"])


@router_2.get("/", response_model=List[CourseResponse])
def list_courses(session: Session = Depends(get_session)):
    """List all courses."""
    items = session.query(Course).all()
    return items


@router_2.get("/{item_id}", response_model=CourseResponse)
def get_course(item_id: int, session: Session = Depends(get_session)):
    """Get a specific Course by ID."""
    item = session.query(Course).filter(Course.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Course not found")
    return item


@router_2.post("/", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
def create_course(data: CourseCreate, session: Session = Depends(get_session)):
    """Create a new Course."""
    # LLM_FILL: Check for existing Enrollment with same keys (duplicate check)
    # LLM_FILL: Apply business rule: Prevent enrollment when the course has reached its maximum capacity. The system must count...
    # LLM_FILL: Apply business rule: Prevent a student from enrolling in the same course more than once. The system must check for...
    # LLM_FILL: Validate create_course logic
    if data.capacity < 1:
        raise HTTPException(status_code=422, detail="Course capacity must be at least 1")
    item = Course(**data.model_dump())
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@router_2.put("/{item_id}", response_model=CourseResponse)
def update_course(item_id: int, data: CourseUpdate, session: Session = Depends(get_session)):
    """Update an existing Course."""
    item = session.query(Course).filter(Course.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Course not found")
    # LLM_FILL: Validate update_course logic
    if data.capacity is not None and data.capacity < 1:
        raise HTTPException(status_code=422, detail="Course capacity must be at least 1")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(item, key, value)
    session.commit()
    session.refresh(item)
    return item


@router_2.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(item_id: int, session: Session = Depends(get_session)):
    """Delete a Course."""
    item = session.query(Course).filter(Course.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Course not found")
    # LLM_FILL: Validate delete_course logic (cascade checks)
    enrollments = session.query(Enrollment).filter(Enrollment.course_id == item_id).all()
    for enrollment in enrollments:
        session.delete(enrollment)
    session.delete(item)
    session.commit()


router_3 = APIRouter(prefix="/enrollments", tags=["Enrollment"])


@router_3.get("/", response_model=List[EnrollmentResponse])
def list_enrollments(session: Session = Depends(get_session)):
    """List all enrollments."""
    items = session.query(Enrollment).all()
    return items


@router_3.get("/{item_id}", response_model=EnrollmentResponse)
def get_enrollment(item_id: int, session: Session = Depends(get_session)):
    """Get a specific Enrollment by ID."""
    item = session.query(Enrollment).filter(Enrollment.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return item


@router_3.post("/", response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED)
def create_enrollment(data: EnrollmentCreate, session: Session = Depends(get_session)):
    """Create a new Enrollment."""
    # LLM_FILL: Apply business rule: Prevent enrollment when the course has reached its maximum capacity. The system must count...
    # LLM_FILL: Apply business rule: Prevent a student from enrolling in the same course more than once. The system must check for...
    # LLM_FILL: Validate create_enrollment logic
    # Check existence of student and course
    student = session.query(Student).filter(Student.id == data.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    course = session.query(Course).filter(Course.id == data.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # Duplicate enrollment check
    existing = session.query(Enrollment).filter(
        Enrollment.student_id == data.student_id,
        Enrollment.course_id == data.course_id
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail="Student is already enrolled in this course")

    # Capacity check
    enrollment_count = session.query(Enrollment).filter(Enrollment.course_id == data.course_id).count()
    if enrollment_count >= course.capacity:
        raise HTTPException(status_code=409, detail="Course has reached maximum capacity")

    # Build object and set enrolled_at if not provided
    item_data = data.model_dump()
    if 'enrolled_at' not in item_data or item_data.get('enrolled_at') is None:
        from datetime import datetime
        item_data['enrolled_at'] = datetime.utcnow()
    item = Enrollment(**item_data)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@router_3.put("/{item_id}", response_model=EnrollmentResponse)
def update_enrollment(item_id: int, data: EnrollmentUpdate, session: Session = Depends(get_session)):
    """Update an existing Enrollment."""
    item = session.query(Enrollment).filter(Enrollment.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    # LLM_FILL: Validate update_enrollment logic
    # Prevent changing student or course after creation
    updated = data.model_dump(exclude_unset=True)
    if 'student_id' in updated or 'course_id' in updated:
        raise HTTPException(status_code=422, detail="Student and course cannot be changed after enrollment")
    for key, value in updated.items():
        setattr(item, key, value)
    session.commit()
    session.refresh(item)
    return item


@router_3.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_enrollment(item_id: int, session: Session = Depends(get_session)):
    """Delete a Enrollment."""
    item = session.query(Enrollment).filter(Enrollment.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    # LLM_FILL: Validate delete_enrollment logic (cascade checks)
    session.delete(item)
    session.commit()


# Collect all routers
routers = [
    router_1,
    router_2,
    router_3,
]