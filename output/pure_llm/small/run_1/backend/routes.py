from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from models import Student, Course, Enrollment
from schemas import (
    StudentCreate, StudentUpdate, StudentResponse,
    CourseCreate, CourseUpdate, CourseResponse,
    EnrollmentCreate, EnrollmentResponse, EnrollmentListResponse
)
from database import get_db

router = APIRouter()

# Student Routes
@router.post("/students/", response_model=StudentResponse, status_code=201)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    # Check if email already exists
    existing_student = db.query(Student).filter(Student.email == student.email).first()
    if existing_student:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    db_student = Student(name=student.name, email=student.email)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@router.get("/students/", response_model=List[StudentResponse])
def get_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    students = db.query(Student).offset(skip).limit(limit).all()
    return students

@router.get("/students/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.put("/students/{student_id}", response_model=StudentResponse)
def update_student(student_id: int, student: StudentUpdate, db: Session = Depends(get_db)):
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    if student.email is not None:
        existing = db.query(Student).filter(Student.email == student.email, Student.id != student_id).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")
        db_student.email = student.email
    
    if student.name is not None:
        db_student.name = student.name
    
    db.commit()
    db.refresh(db_student)
    return db_student

@router.delete("/students/{student_id}", status_code=204)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Delete all enrollments for this student
    db.query(Enrollment).filter(Enrollment.student_id == student_id).delete()
    db.delete(db_student)
    db.commit()
    return None

# Course Routes
@router.post("/courses/", response_model=CourseResponse, status_code=201)
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    db_course = Course(
        title=course.title,
        description=course.description,
        capacity=course.capacity
    )
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    
    # Calculate enrolled count
    enrolled_count = db.query(Enrollment).filter(Enrollment.course_id == db_course.id).count()
    response = CourseResponse(
        id=db_course.id,
        title=db_course.title,
        description=db_course.description,
        capacity=db_course.capacity,
        enrolled_count=enrolled_count
    )
    return response

@router.get("/courses/", response_model=List[CourseResponse])
def get_courses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    courses = db.query(Course).offset(skip).limit(limit).all()
    result = []
    for course in courses:
        enrolled_count = db.query(Enrollment).filter(Enrollment.course_id == course.id).count()
        result.append(CourseResponse(
            id=course.id,
            title=course.title,
            description=course.description,
            capacity=course.capacity,
            enrolled_count=enrolled_count
        ))
    return result

@router.get("/courses/{course_id}", response_model=CourseResponse)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    enrolled_count = db.query(Enrollment).filter(Enrollment.course_id == course.id).count()
    return CourseResponse(
        id=course.id,
        title=course.title,
        description=course.description,
        capacity=course.capacity,
        enrolled_count=enrolled_count
    )

@router.put("/courses/{course_id}", response_model=CourseResponse)
def update_course(course_id: int, course: CourseUpdate, db: Session = Depends(get_db)):
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    if course.title is not None:
        db_course.title = course.title
    if course.description is not None:
        db_course.description = course.description
    if course.capacity is not None:
        # Check if new capacity is less than current enrollments
        enrolled_count = db.query(Enrollment).filter(Enrollment.course_id == course_id).count()
        if course.capacity < enrolled_count:
            raise HTTPException(
                status_code=400,
                detail=f"Cannot reduce capacity below current enrollment count ({enrolled_count})"
            )
        db_course.capacity = course.capacity
    
    db.commit()
    db.refresh(db_course)
    
    enrolled_count = db.query(Enrollment).filter(Enrollment.course_id == db_course.id).count()
    return CourseResponse(
        id=db_course.id,
        title=db_course.title,
        description=db_course.description,
        capacity=db_course.capacity,
        enrolled_count=enrolled_count
    )

@router.delete("/courses/{course_id}", status_code=204)
def delete_course(course_id: int, db: Session = Depends(get_db)):
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Delete all enrollments for this course
    db.query(Enrollment).filter(Enrollment.course_id == course_id).delete()
    db.delete(db_course)
    db.commit()
    return None

# Enrollment Routes
@router.post("/enrollments/", response_model=EnrollmentResponse, status_code=201)
def create_enrollment(enrollment: EnrollmentCreate, db: Session = Depends(get_db)):
    # Check if student exists
    student = db.query(Student).filter(Student.id == enrollment.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Check if course exists
    course = db.query(Course).filter(Course.id == enrollment.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Business Rule: duplicate_enrollment
    existing_enrollment = db.query(Enrollment).filter(
        Enrollment.student_id == enrollment.student_id,
        Enrollment.course_id == enrollment.course_id
    ).first()
    if existing_enrollment:
        raise HTTPException(status_code=400, detail="Student is already enrolled in this course")
    
    # Business Rule: capacity_check
    current_enrollments = db.query(Enrollment).filter(Enrollment.course_id == enrollment.course_id).count()
    if current_enrollments >= course.capacity:
        raise HTTPException(
            status_code=400,
            detail=f"Course is at full capacity ({current_enrollments}/{course.capacity})"
        )
    
    # Create enrollment
    db_enrollment = Enrollment(
        student_id=enrollment.student_id,
        course_id=enrollment.course_id,
        enrolled_at=datetime.utcnow()
    )
    db.add(db_enrollment)
    db.commit()
    db.refresh(db_enrollment)
    
    return EnrollmentResponse(
        id=db_enrollment.id,
        student_id=db_enrollment.student_id,
        course_id=db_enrollment.course_id,
        enrolled_at=db_enrollment.enrolled_at,
        student_name=student.name,
        course_title=course.title
    )

@router.get("/enrollments/", response_model=List[EnrollmentListResponse])
def get_enrollments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    enrollments = db.query(Enrollment).offset(skip).limit(limit).all()
    result = []
    for enrollment in enrollments:
        student = db.query(Student).filter(Student.id == enrollment.student_id).first()
        course = db.query(Course).filter(Course.id == enrollment.course_id).first()
        result.append(EnrollmentListResponse(
            id=enrollment.id,
            student_id=enrollment.student_id,
            course_id=enrollment.course_id,
            enrolled_at=enrollment.enrolled_at,
            student_name=student.name if student else "Unknown",
            course_title=course.title if course else "Unknown"
        ))
    return result

@router.get("/enrollments/{enrollment_id}", response_model=EnrollmentResponse)
def get_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    enrollment = db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    
    student = db.query(Student).filter(Student.id == enrollment.student_id).first()
    course = db.query(Course).filter(Course.id == enrollment.course_id).first()
    
    return EnrollmentResponse(
        id=enrollment.id,
        student_id=enrollment.student_id,
        course_id=enrollment.course_id,
        enrolled_at=enrollment.enrolled_at,
        student_name=student.name if student else "Unknown",
        course_title=course.title if course else "Unknown"
    )

@router.delete("/enrollments/{enrollment_id}", status_code=204)
def delete_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    db_enrollment = db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()
    if not db_enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    
    db.delete(db_enrollment)
    db.commit()
    return None

@router.get("/students/{student_id}/enrollments/", response_model=List[EnrollmentListResponse])
def get_student_enrollments(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    enrollments = db.query(Enrollment).filter(Enrollment.student_id == student_id).all()
    result = []
    for enrollment in enrollments:
        course = db.query(Course).filter(Course.id == enrollment.course_id).first()
        result.append(EnrollmentListResponse(
            id=enrollment.id,
            student_id=enrollment.student_id,
            course_id=enrollment.course_id,
            enrolled_at=enrollment.enrolled_at,
            student_name=student.name,
            course_title=course.title if course else "Unknown"
        ))
    return result

@router.get("/courses/{course_id}/enrollments/", response_model=List[EnrollmentListResponse])
def get_course_enrollments(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    enrollments = db.query(Enrollment).filter(Enrollment.course_id == course_id).all()
    result = []
    for enrollment in enrollments:
        student = db.query(Student).filter(Student.id == enrollment.student_id).first()
        result.append(EnrollmentListResponse(
            id=enrollment.id,
            student_id=enrollment.student_id,
            course_id=enrollment.course_id,
            enrolled_at=enrollment.enrolled_at,
            student_name=student.name if student else "Unknown",
            course_title=course.title
        ))
    return result