from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas
from .database import get_db

router = APIRouter()

# ---------- Student Endpoints ----------
@router.get("/students", response_model=List[schemas.StudentOut])
def get_students(db: Session = Depends(get_db)):
    return db.query(models.Student).all()

@router.get("/students/{student_id}", response_model=schemas.StudentOut)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.post("/students", response_model=schemas.StudentOut, status_code=status.HTTP_201_CREATED)
def create_student(student_in: schemas.StudentCreate, db: Session = Depends(get_db)):
    # Check email uniqueness (already in DB unique constraint, but handle gracefully)
    existing = db.query(models.Student).filter(models.Student.email == student_in.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    student = models.Student(**student_in.dict())
    db.add(student)
    db.commit()
    db.refresh(student)
    return student

@router.put("/students/{student_id}", response_model=schemas.StudentOut)
def update_student(student_id: int, student_up: schemas.StudentUpdate, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    update_data = student_up.dict(exclude_unset=True)
    # If email changed, check uniqueness
    if "email" in update_data:
        existing = db.query(models.Student).filter(models.Student.email == update_data["email"], models.Student.id != student_id).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already taken")
    for key, value in update_data.items():
        setattr(student, key, value)
    db.commit()
    db.refresh(student)
    return student

@router.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(student)
    db.commit()
    return None

# ---------- Course Endpoints ----------
@router.get("/courses", response_model=List[schemas.CourseOut])
def get_courses(db: Session = Depends(get_db)):
    return db.query(models.Course).all()

@router.get("/courses/{course_id}", response_model=schemas.CourseOut)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.post("/courses", response_model=schemas.CourseOut, status_code=status.HTTP_201_CREATED)
def create_course(course_in: schemas.CourseCreate, db: Session = Depends(get_db)):
    course = models.Course(**course_in.dict())
    db.add(course)
    db.commit()
    db.refresh(course)
    return course

@router.put("/courses/{course_id}", response_model=schemas.CourseOut)
def update_course(course_id: int, course_up: schemas.CourseUpdate, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    update_data = course_up.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(course, key, value)
    db.commit()
    db.refresh(course)
    return course

@router.delete("/courses/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    db.delete(course)
    db.commit()
    return None

# ---------- Enrollment Endpoints ----------
@router.post("/enrollments", response_model=schemas.EnrollmentOut, status_code=status.HTTP_201_CREATED)
def create_enrollment(enrollment_in: schemas.EnrollmentCreate, db: Session = Depends(get_db)):
    # Validate student and course exist
    student = db.query(models.Student).filter(models.Student.id == enrollment_in.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    course = db.query(models.Course).filter(models.Course.id == enrollment_in.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # Duplicate enrollment check
    existing = db.query(models.Enrollment).filter(
        models.Enrollment.student_id == enrollment_in.student_id,
        models.Enrollment.course_id == enrollment_in.course_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Student already enrolled in this course")

    # Capacity check: count current enrollments
    current_count = db.query(models.Enrollment).filter(models.Enrollment.course_id == enrollment_in.course_id).count()
    if current_count >= course.capacity:
        raise HTTPException(status_code=400, detail="Course has reached its maximum capacity")

    enrollment = models.Enrollment(student_id=enrollment_in.student_id, course_id=enrollment_in.course_id)
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    # Refresh to include relationships
    db.refresh(enrollment)
    return enrollment

@router.get("/enrollments", response_model=List[schemas.EnrollmentOut])
def get_enrollments(db: Session = Depends(get_db)):
    return db.query(models.Enrollment).all()

@router.delete("/enrollments/{enrollment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    enrollment = db.query(models.Enrollment).filter(models.Enrollment.id == enrollment_id).first()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    db.delete(enrollment)
    db.commit()
    return None