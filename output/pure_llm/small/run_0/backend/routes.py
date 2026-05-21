from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import SessionLocal, Student, Course, Enrollment
from schemas import StudentCreate, StudentResponse, CourseCreate, CourseResponse, EnrollmentCreate, EnrollmentResponse
from typing import List, Optional

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Student CRUD ---
@router.post("/students/", response_model=StudentResponse, status_code=201)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    # check duplicate email
    db_student = db.query(Student).filter(Student.email == student.email).first()
    if db_student:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_student = Student(name=student.name, email=student.email)
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

@router.get("/students/", response_model=List[StudentResponse])
def list_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    students = db.query(Student).offset(skip).limit(limit).all()
    return students

@router.get("/students/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.put("/students/{student_id}", response_model=StudentResponse)
def update_student(student_id: int, student_data: StudentCreate, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    # check email uniqueness if changed
    existing = db.query(Student).filter(Student.email == student_data.email, Student.id != student_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already in use")
    student.name = student_data.name
    student.email = student_data.email
    db.commit()
    db.refresh(student)
    return student

@router.delete("/students/{student_id}", status_code=204)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(student)
    db.commit()
    return None

# --- Course CRUD ---
@router.post("/courses/", response_model=CourseResponse, status_code=201)
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    new_course = Course(title=course.title, description=course.description, capacity=course.capacity)
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return course_response(new_course, db)

@router.get("/courses/", response_model=List[CourseResponse])
def list_courses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    courses = db.query(Course).offset(skip).limit(limit).all()
    return [course_response(c, db) for c in courses]

@router.get("/courses/{course_id}", response_model=CourseResponse)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course_response(course, db)

@router.put("/courses/{course_id}", response_model=CourseResponse)
def update_course(course_id: int, course_data: CourseCreate, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    course.title = course_data.title
    course.description = course_data.description
    course.capacity = course_data.capacity
    db.commit()
    db.refresh(course)
    return course_response(course, db)

@router.delete("/courses/{course_id}", status_code=204)
def delete_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    db.delete(course)
    db.commit()
    return None

# --- Enrollment operations ---
@router.post("/enrollments/", response_model=EnrollmentResponse, status_code=201)
def create_enrollment(enrollment: EnrollmentCreate, db: Session = Depends(get_db)):
    # Check student exists
    student = db.query(Student).filter(Student.id == enrollment.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    # Check course exists
    course = db.query(Course).filter(Course.id == enrollment.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    # Business rule: capacity check
    current_count = db.query(Enrollment).filter(Enrollment.course_id == enrollment.course_id).count()
    if current_count >= course.capacity:
        raise HTTPException(status_code=400, detail="Course is at full capacity")
    # Business rule: duplicate enrollment check (plus DB unique constraint)
    existing = db.query(Enrollment).filter(
        Enrollment.student_id == enrollment.student_id,
        Enrollment.course_id == enrollment.course_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Student already enrolled in this course")
    new_enrollment = Enrollment(student_id=enrollment.student_id, course_id=enrollment.course_id)
    db.add(new_enrollment)
    db.commit()
    db.refresh(new_enrollment)
    # Load relationships for response
    return enrollment_response(new_enrollment, db)

@router.get("/enrollments/", response_model=List[EnrollmentResponse])
def list_enrollments(
    student_id: Optional[int] = None,
    course_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(Enrollment)
    if student_id is not None:
        query = query.filter(Enrollment.student_id == student_id)
    if course_id is not None:
        query = query.filter(Enrollment.course_id == course_id)
    enrollments = query.offset(skip).limit(limit).all()
    return [enrollment_response(e, db) for e in enrollments]

@router.delete("/enrollments/{enrollment_id}", status_code=204)
def delete_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    enrollment = db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    db.delete(enrollment)
    db.commit()
    return None

# Helper functions to build response with computed fields
def course_response(course: Course, db: Session) -> dict:
    count = db.query(Enrollment).filter(Enrollment.course_id == course.id).count()
    return {
        "id": course.id,
        "title": course.title,
        "description": course.description,
        "capacity": course.capacity,
        "current_enrollment": count
    }

def enrollment_response(enrollment: Enrollment, db: Session) -> dict:
    # eager load relationships
    student = db.query(Student).filter(Student.id == enrollment.student_id).first()
    course = db.query(Course).filter(Course.id == enrollment.course_id).first()
    count = db.query(Enrollment).filter(Enrollment.course_id == course.id).count()
    return {
        "id": enrollment.id,
        "student_id": enrollment.student_id,
        "course_id": enrollment.course_id,
        "enrolled_at": enrollment.enrolled_at,
        "student": {
            "id": student.id,
            "name": student.name,
            "email": student.email,
        },
        "course": {
            "id": course.id,
            "title": course.title,
            "description": course.description,
            "capacity": course.capacity,
            "current_enrollment": count,
        }
    }