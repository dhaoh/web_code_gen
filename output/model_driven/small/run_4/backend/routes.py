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
    # No enrollment-related checks required for Student creation.
    # LLM_FILL: Apply business rule: Prevent a student from enrolling in the same course more than once. The system must check for...
    # Business rule applies to Enrollment, not Student.
    # LLM_FILL: Validate create_student logic
    # No additional validation needed.
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
    # No additional validation required beyond standard update.
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
    # Cascade delete: remove all enrollments for this student
    session.query(Enrollment).filter(Enrollment.student_id == item_id).delete()
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
    # No enrollment-related checks required for Course creation.
    # LLM_FILL: Apply business rule: Prevent enrollment when the course has reached its maximum capacity. The system must count...
    # Business rule applies to Enrollment, not Course creation.
    # LLM_FILL: Apply business rule: Prevent a student from enrolling in the same course more than once. The system must check for...
    # Business rule applies to Enrollment, not Course creation.
    # LLM_FILL: Validate create_course logic
    # No additional validation needed.
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
    # No additional validation required beyond standard update.
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
    # Cascade delete: remove all enrollments for this course
    session.query(Enrollment).filter(Enrollment.course_id == item_id).delete()
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
    # Check that the course exists and has available capacity
    course = session.query(Course).filter(Course.id == data.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    current_enrollments = session.query(Enrollment).filter(
        Enrollment.course_id == data.course_id
    ).count()
    if current_enrollments >= course.capacity:
        raise HTTPException(
            status_code=409, detail="Course has reached its maximum capacity"
        )
    
    # LLM_FILL: Apply business rule: Prevent a student from enrolling in the same course more than once. The system must check for...
    # Check for duplicate enrollment
    existing = session.query(Enrollment).filter(
        Enrollment.student_id == data.student_id,
        Enrollment.course_id == data.course_id,
    ).first()
    if existing:
        raise HTTPException(
            status_code=409, detail="Student is already enrolled in this course"
        )
    
    # LLM_FILL: Validate create_enrollment logic
    # Ensure the student exists before enrolling
    student = session.query(Student).filter(Student.id == data.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
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
    # If student_id or course_id is changed, recheck duplicate and capacity rules
    changed_student = data.student_id is not None and data.student_id != item.student_id
    changed_course = data.course_id is not None and data.course_id != item.course_id
    
    if changed_student or changed_course:
        new_student_id = data.student_id if changed_student else item.student_id
        new_course_id = data.course_id if changed_course else item.course_id
        
        # Duplicate check with new values
        duplicate = session.query(Enrollment).filter(
            Enrollment.student_id == new_student_id,
            Enrollment.course_id == new_course_id,
            Enrollment.id != item.id
        ).first()
        if duplicate:
            raise HTTPException(
                status_code=409, detail="An enrollment with this student and course already exists"
            )
        
        if changed_course:
            # Ensure new course exists and has room
            course = session.query(Course).filter(Course.id == new_course_id).first()
            if not course:
                raise HTTPException(status_code=404, detail="New course not found")
            current = session.query(Enrollment).filter(
                Enrollment.course_id == new_course_id,
                Enrollment.id != item.id
            ).count()
            if current >= course.capacity:
                raise HTTPException(
                    status_code=409, detail="New course is at full capacity"
                )
    
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
    # No cascade needed; simply delete the enrollment
    session.delete(item)
    session.commit()


# Collect all routers
routers = [
    router_1,
    router_2,
    router_3,
]