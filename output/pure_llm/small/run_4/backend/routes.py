from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional

from . import models, schemas
from .models import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter()

# ---------------------------- Students ----------------------------
@router.get("/students", response_model=List[schemas.StudentResponse])
def list_students(db: Session = Depends(get_db)):
    students = db.query(models.Student).all()
    return students

@router.get("/students/{student_id}", response_model=schemas.StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.post("/students", response_model=schemas.StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Student).filter(models.Student.email == student.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_student = models.Student(name=student.name, email=student.email)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@router.put("/students/{student_id}", response_model=schemas.StudentResponse)
def update_student(student_id: int, student: schemas.StudentUpdate, db: Session = Depends(get_db)):
    db_student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    if student.email != db_student.email:
        existing = db.query(models.Student).filter(models.Student.email == student.email).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already in use")
    db_student.name = student.name
    db_student.email = student.email
    db.commit()
    db.refresh(db_student)
    return db_student

@router.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    db_student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(db_student)
    db.commit()
    return

# ---------------------------- Courses ----------------------------
@router.get("/courses", response_model=List[schemas.CourseResponse])
def list_courses(db: Session = Depends(get_db)):
    courses = db.query(models.Course).all()
    result = []
    for course in courses:
        enrolled_count = db.query(models.Enrollment).filter(models.Enrollment.course_id == course.id).count()
        result.append(schemas.CourseResponse(
            id=course.id,
            title=course.title,
            description=course.description,
            capacity=course.capacity,
            enrolled_count=enrolled_count,
        ))
    return result

@router.get("/courses/{course_id}", response_model=schemas.CourseResponse)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    enrolled_count = db.query(models.Enrollment).filter(models.Enrollment.course_id == course.id).count()
    return schemas.CourseResponse(
        id=course.id,
        title=course.title,
        description=course.description,
        capacity=course.capacity,
        enrolled_count=enrolled_count,
    )

@router.post("/courses", response_model=schemas.CourseResponse, status_code=status.HTTP_201_CREATED)
def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    db_course = models.Course(title=course.title, description=course.description, capacity=course.capacity)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return schemas.CourseResponse(
        id=db_course.id,
        title=db_course.title,
        description=db_course.description,
        capacity=db_course.capacity,
        enrolled_count=0,
    )

@router.put("/courses/{course_id}", response_model=schemas.CourseResponse)
def update_course(course_id: int, course: schemas.CourseUpdate, db: Session = Depends(get_db)):
    db_course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    db_course.title = course.title
    db_course.description = course.description
    db_course.capacity = course.capacity
    db.commit()
    db.refresh(db_course)
    enrolled_count = db.query(models.Enrollment).filter(models.Enrollment.course_id == course_id).count()
    return schemas.CourseResponse(
        id=db_course.id,
        title=db_course.title,
        description=db_course.description,
        capacity=db_course.capacity,
        enrolled_count=enrolled_count,
    )

@router.delete("/courses/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(course_id: int, db: Session = Depends(get_db)):
    db_course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    db.delete(db_course)
    db.commit()
    return

# ---------------------------- Enrollments ----------------------------
@router.get("/enrollments", response_model=List[schemas.EnrollmentResponse])
def list_enrollments(
    student_id: Optional[int] = Query(None),
    course_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(models.Enrollment).options(
        joinedload(models.Enrollment.student),
        joinedload(models.Enrollment.course)
    )
    if student_id:
        query = query.filter(models.Enrollment.student_id == student_id)
    if course_id:
        query = query.filter(models.Enrollment.course_id == course_id)
    enrollments = query.all()
    return enrollments

@router.post("/enrollments", response_model=schemas.EnrollmentResponse, status_code=status.HTTP_201_CREATED)
def create_enrollment(enrollment: schemas.EnrollmentCreate, db: Session = Depends(get_db)):
    # Duplicate check
    existing = db.query(models.Enrollment).filter(
        models.Enrollment.student_id == enrollment.student_id,
        models.Enrollment.course_id == enrollment.course_id,
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail="Enrollment already exists")

    # Validate existence
    course = db.query(models.Course).filter(models.Course.id == enrollment.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    student = db.query(models.Student).filter(models.Student.id == enrollment.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Capacity check
    current_count = db.query(models.Enrollment).filter(models.Enrollment.course_id == enrollment.course_id).count()
    if current_count >= course.capacity:
        raise HTTPException(status_code=400, detail="Course has reached its maximum capacity")

    new_enrollment = models.Enrollment(
        student_id=enrollment.student_id,
        course_id=enrollment.course_id,
    )
    db.add(new_enrollment)
    db.commit()
    db.refresh(new_enrollment)
    # Attach related objects for the response
    new_enrollment.student = student
    new_enrollment.course = course
    return new_enrollment

@router.delete("/enrollments/{enrollment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    enrollment = db.query(models.Enrollment).filter(models.Enrollment.id == enrollment_id).first()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    db.delete(enrollment)
    db.commit()
    return