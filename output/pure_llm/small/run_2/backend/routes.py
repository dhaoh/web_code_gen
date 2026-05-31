from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal
from models import Student, Course, Enrollment
from schemas import (
    StudentCreate, StudentUpdate, StudentOut,
    CourseCreate, CourseUpdate, CourseOut,
    EnrollmentCreate, EnrollmentOut, EnrollmentDetail
)
import datetime

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------- Student endpoints ----------
@router.get("/students", response_model=List[StudentOut])
def list_students(db: Session = Depends(get_db)):
    return db.query(Student).all()

@router.post("/students", response_model=StudentOut, status_code=status.HTTP_201_CREATED)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    existing = db.query(Student).filter(Student.email == student.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")
    db_student = Student(name=student.name, email=student.email)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@router.get("/students/{student_id}", response_model=StudentOut)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.put("/students/{student_id}", response_model=StudentOut)
def update_student(student_id: int, student: StudentUpdate, db: Session = Depends(get_db)):
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    if student.email != db_student.email:
        existing = db.query(Student).filter(Student.email == student.email).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already in use")
    db_student.name = student.name
    db_student.email = student.email
    db.commit()
    db.refresh(db_student)
    return db_student

@router.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(student)
    db.commit()
    return

# ---------- Course endpoints ----------
@router.get("/courses", response_model=List[CourseOut])
def list_courses(db: Session = Depends(get_db)):
    courses = db.query(Course).all()
    result = []
    for c in courses:
        enrolled = db.query(Enrollment).filter(Enrollment.course_id == c.id).count()
        course_out = CourseOut(
            id=c.id,
            title=c.title,
            description=c.description,
            capacity=c.capacity,
            enrolled_count=enrolled
        )
        result.append(course_out)
    return result

@router.post("/courses", response_model=CourseOut, status_code=status.HTTP_201_CREATED)
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    db_course = Course(title=course.title, description=course.description, capacity=course.capacity)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return CourseOut(
        id=db_course.id,
        title=db_course.title,
        description=db_course.description,
        capacity=db_course.capacity,
        enrolled_count=0
    )

@router.get("/courses/{course_id}", response_model=CourseOut)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    enrolled = db.query(Enrollment).filter(Enrollment.course_id == course_id).count()
    return CourseOut(
        id=course.id,
        title=course.title,
        description=course.description,
        capacity=course.capacity,
        enrolled_count=enrolled
    )

@router.put("/courses/{course_id}", response_model=CourseOut)
def update_course(course_id: int, course: CourseUpdate, db: Session = Depends(get_db)):
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    db_course.title = course.title
    db_course.description = course.description
    db_course.capacity = course.capacity
    db.commit()
    db.refresh(db_course)
    enrolled = db.query(Enrollment).filter(Enrollment.course_id == course_id).count()
    return CourseOut(
        id=db_course.id,
        title=db_course.title,
        description=db_course.description,
        capacity=db_course.capacity,
        enrolled_count=enrolled
    )

@router.delete("/courses/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    db.delete(course)
    db.commit()
    return

# ---------- Enrollment endpoints ----------
@router.post("/enrollments", response_model=EnrollmentDetail, status_code=status.HTTP_201_CREATED)
def create_enrollment(enrollment: EnrollmentCreate, db: Session = Depends(get_db)):
    # Check student and course exist
    student = db.query(Student).filter(Student.id == enrollment.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    course = db.query(Course).filter(Course.id == enrollment.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Duplicate check
    existing = db.query(Enrollment).filter(
        Enrollment.student_id == enrollment.student_id,
        Enrollment.course_id == enrollment.course_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Student is already enrolled in this course")
    
    # Capacity check
    enrolled_count = db.query(Enrollment).filter(Enrollment.course_id == enrollment.course_id).count()
    if enrolled_count >= course.capacity:
        raise HTTPException(status_code=400, detail="Course has reached its capacity")
    
    db_enrollment = Enrollment(
        student_id=enrollment.student_id,
        course_id=enrollment.course_id,
        enrolled_at=datetime.datetime.utcnow()
    )
    db.add(db_enrollment)
    db.commit()
    db.refresh(db_enrollment)
    # Return with relationships
    enrolled = db.query(Enrollment).filter(Enrollment.course_id == course.id).count()
    course_out = CourseOut(
        id=course.id,
        title=course.title,
        description=course.description,
        capacity=course.capacity,
        enrolled_count=enrolled
    )
    return EnrollmentDetail(
        id=db_enrollment.id,
        student_id=db_enrollment.student_id,
        course_id=db_enrollment.course_id,
        enrolled_at=db_enrollment.enrolled_at,
        student=StudentOut(id=student.id, name=student.name, email=student.email),
        course=course_out
    )

@router.delete("/enrollments/{enrollment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    enrollment = db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    db.delete(enrollment)
    db.commit()
    return

@router.get("/enrollments", response_model=List[EnrollmentDetail])
def list_enrollments(student_id: int = None, db: Session = Depends(get_db)):
    query = db.query(Enrollment)
    if student_id is not None:
        query = query.filter(Enrollment.student_id == student_id)
    enrollments = query.all()
    result = []
    for e in enrollments:
        course = e.course
        enrolled_count = db.query(Enrollment).filter(Enrollment.course_id == course.id).count()
        course_out = CourseOut(
            id=course.id,
            title=course.title,
            description=course.description,
            capacity=course.capacity,
            enrolled_count=enrolled_count
        )
        student_out = StudentOut(id=e.student.id, name=e.student.name, email=e.student.email)
        result.append(EnrollmentDetail(
            id=e.id,
            student_id=e.student_id,
            course_id=e.course_id,
            enrolled_at=e.enrolled_at,
            student=student_out,
            course=course_out
        ))
    return result