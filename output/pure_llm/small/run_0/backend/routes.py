from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from datetime import datetime

from . import models, schemas
from .database import get_db

router = APIRouter()

# Student Routes
@router.post("/students/", response_model=schemas.StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    # Check if email already exists
    existing_student = db.query(models.Student).filter(models.Student.email == student.email).first()
    if existing_student:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Student with email {student.email} already exists"
        )
    
    db_student = models.Student(name=student.name, email=student.email)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@router.get("/students/", response_model=List[schemas.StudentResponse])
def get_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    students = db.query(models.Student).offset(skip).limit(limit).all()
    return students

@router.get("/students/{student_id}", response_model=schemas.StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with id {student_id} not found"
        )
    return student

@router.put("/students/{student_id}", response_model=schemas.StudentResponse)
def update_student(student_id: int, student_update: schemas.StudentUpdate, db: Session = Depends(get_db)):
    db_student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not db_student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with id {student_id} not found"
        )
    
    # Check email uniqueness if updating email
    if student_update.email and student_update.email != db_student.email:
        existing = db.query(models.Student).filter(models.Student.email == student_update.email).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Student with email {student_update.email} already exists"
            )
    
    if student_update.name is not None:
        db_student.name = student_update.name
    if student_update.email is not None:
        db_student.email = student_update.email
    
    db.commit()
    db.refresh(db_student)
    return db_student

@router.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    db_student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not db_student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with id {student_id} not found"
        )
    
    # Delete all enrollments for this student
    db.query(models.Enrollment).filter(models.Enrollment.student_id == student_id).delete()
    db.delete(db_student)
    db.commit()
    return None

# Course Routes
@router.post("/courses/", response_model=schemas.CourseResponse, status_code=status.HTTP_201_CREATED)
def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    db_course = models.Course(
        title=course.title,
        description=course.description,
        capacity=course.capacity
    )
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    
    # Calculate enrolled count
    enrolled_count = db.query(models.Enrollment).filter(
        models.Enrollment.course_id == db_course.id
    ).count()
    db_course.enrolled_count = enrolled_count
    
    return db_course

@router.get("/courses/", response_model=List[schemas.CourseResponse])
def get_courses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    courses = db.query(models.Course).offset(skip).limit(limit).all()
    
    # Add enrolled_count to each course
    for course in courses:
        course.enrolled_count = db.query(models.Enrollment).filter(
            models.Enrollment.course_id == course.id
        ).count()
    
    return courses

@router.get("/courses/{course_id}", response_model=schemas.CourseResponse)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with id {course_id} not found"
        )
    
    course.enrolled_count = db.query(models.Enrollment).filter(
        models.Enrollment.course_id == course.id
    ).count()
    
    return course

@router.put("/courses/{course_id}", response_model=schemas.CourseResponse)
def update_course(course_id: int, course_update: schemas.CourseUpdate, db: Session = Depends(get_db)):
    db_course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not db_course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with id {course_id} not found"
        )
    
    if course_update.title is not None:
        db_course.title = course_update.title
    if course_update.description is not None:
        db_course.description = course_update.description
    if course_update.capacity is not None:
        # Check if new capacity is less than current enrollments
        current_enrolled = db.query(models.Enrollment).filter(
            models.Enrollment.course_id == course_id
        ).count()
        if course_update.capacity < current_enrolled:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot reduce capacity below current enrollment count ({current_enrolled})"
            )
        db_course.capacity = course_update.capacity
    
    db.commit()
    db.refresh(db_course)
    
    db_course.enrolled_count = db.query(models.Enrollment).filter(
        models.Enrollment.course_id == db_course.id
    ).count()
    
    return db_course

@router.delete("/courses/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(course_id: int, db: Session = Depends(get_db)):
    db_course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not db_course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with id {course_id} not found"
        )
    
    # Delete all enrollments for this course
    db.query(models.Enrollment).filter(models.Enrollment.course_id == course_id).delete()
    db.delete(db_course)
    db.commit()
    return None

# Enrollment Routes
@router.post("/enrollments/", response_model=schemas.EnrollmentResponse, status_code=status.HTTP_201_CREATED)
def create_enrollment(enrollment: schemas.EnrollmentCreate, db: Session = Depends(get_db)):
    # Check if student exists
    student = db.query(models.Student).filter(models.Student.id == enrollment.student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with id {enrollment.student_id} not found"
        )
    
    # Check if course exists
    course = db.query(models.Course).filter(models.Course.id == enrollment.course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with id {enrollment.course_id} not found"
        )
    
    # Business Rule: duplicate_enrollment - Check for existing enrollment
    existing_enrollment = db.query(models.Enrollment).filter(
        models.Enrollment.student_id == enrollment.student_id,
        models.Enrollment.course_id == enrollment.course_id
    ).first()
    
    if existing_enrollment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Student is already enrolled in this course"
        )
    
    # Business Rule: capacity_check - Check course capacity
    current_enrolled = db.query(models.Enrollment).filter(
        models.Enrollment.course_id == enrollment.course_id
    ).count()
    
    if current_enrolled >= course.capacity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Course has reached maximum capacity ({course.capacity})"
        )
    
    # Create enrollment
    db_enrollment = models.Enrollment(
        student_id=enrollment.student_id,
        course_id=enrollment.course_id,
        enrolled_at=datetime.utcnow()
    )
    db.add(db_enrollment)
    db.commit()
    db.refresh(db_enrollment)
    
    # Load relationships
    db_enrollment.student = student
    db_enrollment.course = course
    
    return db_enrollment

@router.get("/enrollments/", response_model=List[schemas.EnrollmentResponse])
def get_enrollments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    enrollments = db.query(models.Enrollment).offset(skip).limit(limit).all()
    return enrollments

@router.get("/enrollments/{enrollment_id}", response_model=schemas.EnrollmentResponse)
def get_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    enrollment = db.query(models.Enrollment).filter(models.Enrollment.id == enrollment_id).first()
    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Enrollment with id {enrollment_id} not found"
        )
    return enrollment

@router.delete("/enrollments/{enrollment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    db_enrollment = db.query(models.Enrollment).filter(models.Enrollment.id == enrollment_id).first()
    if not db_enrollment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Enrollment with id {enrollment_id} not found"
        )
    
    db.delete(db_enrollment)
    db.commit()
    return None

# Additional endpoints for getting enrollments by student or course
@router.get("/students/{student_id}/enrollments/", response_model=List[schemas.EnrollmentResponse])
def get_student_enrollments(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with id {student_id} not found"
        )
    
    enrollments = db.query(models.Enrollment).filter(
        models.Enrollment.student_id == student_id
    ).all()
    return enrollments

@router.get("/courses/{course_id}/enrollments/", response_model=List[schemas.EnrollmentResponse])
def get_course_enrollments(course_id: int, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with id {course_id} not found"
        )
    
    enrollments = db.query(models.Enrollment).filter(
        models.Enrollment.course_id == course_id
    ).all()
    return enrollments