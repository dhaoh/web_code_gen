from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime
from ..database import get_db
from ..models import Enrollment, Student, Course
from ..schemas import EnrollmentCreate, EnrollmentOut

router = APIRouter()

@router.get("/", response_model=List[EnrollmentOut])
def list_enrollments(
    student_id: Optional[int] = None,
    course_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Enrollment)
    if student_id is not None:
        query = query.filter(Enrollment.student_id == student_id)
    if course_id is not None:
        query = query.filter(Enrollment.course_id == course_id)
    enrollments = query.all()
    result = []
    for e in enrollments:
        # Populate joined attributes
        e.student_name = e.student.name if e.student else "Unknown"
        e.course_title = e.course.title if e.course else "Unknown"
        result.append(e)
    return result

@router.post("/", response_model=EnrollmentOut, status_code=201)
def create_enrollment(enrollment: EnrollmentCreate, db: Session = Depends(get_db)):
    # Check student and course exist
    student = db.query(Student).filter(Student.id == enrollment.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    course = db.query(Course).filter(Course.id == enrollment.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # Business rule: duplicate check
    existing = db.query(Enrollment).filter(
        Enrollment.student_id == enrollment.student_id,
        Enrollment.course_id == enrollment.course_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Student is already enrolled in this course")

    # Business rule: capacity check
    current_count = db.query(func.count(Enrollment.id)).filter(
        Enrollment.course_id == enrollment.course_id
    ).scalar()
    if current_count >= course.capacity:
        raise HTTPException(status_code=400, detail="Course has reached its maximum capacity")

    db_enrollment = Enrollment(
        student_id=enrollment.student_id,
        course_id=enrollment.course_id,
        enrolled_at=datetime.utcnow()  # Override server_default if needed
    )
    db.add(db_enrollment)
    db.commit()
    db.refresh(db_enrollment)
    # Make sure relationships are loaded
    db_enrollment.student_name = db_enrollment.student.name
    db_enrollment.course_title = db_enrollment.course.title
    return db_enrollment

@router.delete("/{enrollment_id}", status_code=204)
def delete_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    enrollment = db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    db.delete(enrollment)
    db.commit()
    return None