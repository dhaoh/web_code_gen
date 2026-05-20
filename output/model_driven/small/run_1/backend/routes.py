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
        raise HTTPException(status_code=409, detail="Student with this email already exists")
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
    if data.email is not None:
        existing = session.query(Student).filter(Student.email == data.email, Student.id != item_id).first()
        if existing:
            raise HTTPException(status_code=409, detail="Email already in use by another student")
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
    if enrollments:
        raise HTTPException(status_code=400, detail="Cannot delete student with active enrollments")
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
    existing = session.query(Course).filter(Course.title == data.title).first()
    if existing:
        raise HTTPException(status_code=409, detail="Course with this title already exists")
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
    if data.title is not None:
        existing = session.query(Course).filter(Course.title == data.title, Course.id != item_id).first()
        if existing:
            raise HTTPException(status_code=409, detail="Title already in use by another course")
    if data.capacity is not None and data.capacity < 1:
        raise HTTPException(status_code=422, detail="Course capacity must be at least 1")
    if data.capacity is not None:
        current_enrollments = session.query(Enrollment).filter(Enrollment.course_id == item_id).count()
        if data.capacity < current_enrollments:
            raise HTTPException(status_code=400, detail="Cannot reduce capacity below current enrollment count")
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
    if enrollments:
        raise HTTPException(status_code=400, detail="Cannot delete course with active enrollments")
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
    student = session.query(Student).filter(Student.id == data.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    course = session.query(Course).filter(Course.id == data.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    existing_enrollment = session.query(Enrollment).filter(
        Enrollment.student_id == data.student_id,
        Enrollment.course_id == data.course_id
    ).first()
    if existing_enrollment:
        raise HTTPException(status_code=409, detail="Student is already enrolled in this course")
    current_count = session.query(Enrollment).filter(Enrollment.course_id == data.course_id).count()
    if current_count >= course.capacity:
        raise HTTPException(status_code=400, detail="Course has reached maximum capacity")
    item = Enrollment(**data.model_dump())
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
    if data.student_id is not None or data.course_id is not None:
        new_student_id = data.student_id if data.student_id is not None else item.student_id
        new_course_id = data.course_id if data.course_id is not None else item.course_id
        if data.student_id is not None:
            student = session.query(Student).filter(Student.id == data.student_id).first()
            if not student:
                raise HTTPException(status_code=404, detail="Student not found")
        if data.course_id is not None:
            course = session.query(Course).filter(Course.id == data.course_id).first()
            if not course:
                raise HTTPException(status_code=404, detail="Course not found")
        existing_enrollment = session.query(Enrollment).filter(
            Enrollment.student_id == new_student_id,
            Enrollment.course_id == new_course_id,
            Enrollment.id != item_id
        ).first()
        if existing_enrollment:
            raise HTTPException(status_code=409, detail="This enrollment already exists")
        if data.course_id is not None:
            course = session.query(Course).filter(Course.id == data.course_id).first()
            current_count = session.query(Enrollment).filter(
                Enrollment.course_id == data.course_id,
                Enrollment.id != item_id
            ).count()
            if current_count >= course.capacity:
                raise HTTPException(status_code=400, detail="Course has reached maximum capacity")
    for key, value in data.model_dump(exclude_unset=True).items():
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