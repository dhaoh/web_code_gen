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
    # No business rule requires duplicate check for Student creation
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
    # No business rule requires validation here
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
    # No cascade rules to enforce
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
    # No enrollment-related rules apply here
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
    # No business rule requires validation here
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
    # No cascade rules to enforce
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
    # Business rule: Prevent duplicate enrollment (same student_id, course_id)
    existing = session.query(Enrollment).filter(
        Enrollment.student_id == data.student_id,
        Enrollment.course_id == data.course_id
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail="Student already enrolled in this course")

    # Business rule: Prevent enrollment when course has reached capacity
    course = session.query(Course).filter(Course.id == data.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    current_count = session.query(Enrollment).filter(
        Enrollment.course_id == data.course_id
    ).count()
    if current_count >= course.capacity:
        raise HTTPException(status_code=409, detail="Course has reached maximum capacity")

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
    # No business rule requires validation here
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
    # No cascade rules to enforce
    session.delete(item)
    session.commit()


# Collect all routers
routers = [
    router_1,
    router_2,
    router_3,
]