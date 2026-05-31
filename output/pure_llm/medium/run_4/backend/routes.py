from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from datetime import datetime

router = APIRouter()

def get_db():
    from main import SessionLocal
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---- Helper ----
def calculate_letter_grade(score: float) -> str:
    if score >= 90:
        return 'A'
    elif score >= 80:
        return 'B'
    elif score >= 70:
        return 'C'
    elif score >= 60:
        return 'D'
    else:
        return 'F'

# ---- Users ----
@router.post("/users", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if user.role not in ["student", "teacher"]:
        raise HTTPException(status_code=400, detail="Role must be 'student' or 'teacher'")
    # In production, hash password; here just store as is for simplicity
    db_user = models.User(**user.dict(), password_hash=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/users", response_model=List[schemas.UserResponse])
def list_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

@router.get("/users/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/users/{user_id}", response_model=schemas.UserResponse)
def update_user(user_id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"detail": "User deleted"}

# ---- Departments ----
@router.post("/departments", response_model=schemas.DepartmentResponse)
def create_department(department: schemas.DepartmentCreate, db: Session = Depends(get_db)):
    db_dep = models.Department(**department.dict())
    db.add(db_dep)
    db.commit()
    db.refresh(db_dep)
    return db_dep

@router.get("/departments", response_model=List[schemas.DepartmentResponse])
def list_departments(db: Session = Depends(get_db)):
    return db.query(models.Department).all()

@router.get("/departments/{dep_id}", response_model=schemas.DepartmentResponse)
def get_department(dep_id: int, db: Session = Depends(get_db)):
    dep = db.query(models.Department).filter(models.Department.id == dep_id).first()
    if not dep:
        raise HTTPException(status_code=404, detail="Department not found")
    return dep

@router.put("/departments/{dep_id}", response_model=schemas.DepartmentResponse)
def update_department(dep_id: int, dep_update: schemas.DepartmentCreate, db: Session = Depends(get_db)):
    dep = db.query(models.Department).filter(models.Department.id == dep_id).first()
    if not dep:
        raise HTTPException(status_code=404, detail="Department not found")
    for key, value in dep_update.dict().items():
        setattr(dep, key, value)
    db.commit()
    db.refresh(dep)
    return dep

@router.delete("/departments/{dep_id}")
def delete_department(dep_id: int, db: Session = Depends(get_db)):
    dep = db.query(models.Department).filter(models.Department.id == dep_id).first()
    if not dep:
        raise HTTPException(status_code=404, detail="Department not found")
    db.delete(dep)
    db.commit()
    return {"detail": "Department deleted"}

# ---- Courses ----
@router.post("/courses", response_model=schemas.CourseResponse)
def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    # Validate teacher role if teacher_id provided
    if course.teacher_id:
        teacher = db.query(models.User).filter(models.User.id == course.teacher_id, models.User.role == "teacher").first()
        if not teacher:
            raise HTTPException(status_code=400, detail="Teacher not found or not a teacher")
    db_course = models.Course(**course.dict())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

@router.get("/courses", response_model=List[schemas.CourseResponse])
def list_courses(db: Session = Depends(get_db)):
    return db.query(models.Course).all()

@router.get("/courses/{course_id}", response_model=schemas.CourseResponse)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.put("/courses/{course_id}", response_model=schemas.CourseResponse)
def update_course(course_id: int, course_update: schemas.CourseUpdate, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    update_data = course_update.dict(exclude_unset=True)
    if "teacher_id" in update_data and update_data["teacher_id"] is not None:
        teacher = db.query(models.User).filter(models.User.id == update_data["teacher_id"], models.User.role == "teacher").first()
        if not teacher:
            raise HTTPException(status_code=400, detail="Teacher not found or not a teacher")
    for key, value in update_data.items():
        setattr(course, key, value)
    db.commit()
    db.refresh(course)
    return course

@router.delete("/courses/{course_id}")
def delete_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    db.delete(course)
    db.commit()
    return {"detail": "Course deleted"}

# ---- Enrollments ----
@router.post("/enrollments", response_model=schemas.EnrollmentResponse)
def create_enrollment(enrollment: schemas.EnrollmentCreate, db: Session = Depends(get_db)):
    # Check student role
    student = db.query(models.User).filter(models.User.id == enrollment.student_id, models.User.role == "student").first()
    if not student:
        raise HTTPException(status_code=400, detail="Student not found or not a student")
    # Check duplicate enrollment
    existing = db.query(models.Enrollment).filter(
        models.Enrollment.student_id == enrollment.student_id,
        models.Enrollment.course_id == enrollment.course_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Student already enrolled in this course")
    # Check course capacity
    course = db.query(models.Course).filter(models.Course.id == enrollment.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    current_count = db.query(models.Enrollment).filter(models.Enrollment.course_id == enrollment.course_id).count()
    if current_count >= course.capacity:
        raise HTTPException(status_code=400, detail="Course has reached its maximum capacity")
    # Credit limit check: sum of credits of courses the student is enrolled in
    enrolled_courses = db.query(models.Course).join(models.Enrollment).filter(
        models.Enrollment.student_id == enrollment.student_id
    ).all()
    total_credits = sum(c.credits for c in enrolled_courses) + course.credits
    if total_credits > 30:
        raise HTTPException(status_code=400, detail="Enrolling would exceed the 30-credit limit per semester")
    db_enrollment = models.Enrollment(student_id=enrollment.student_id, course_id=enrollment.course_id)
    db.add(db_enrollment)
    db.commit()
    db.refresh(db_enrollment)
    return db_enrollment

@router.get("/enrollments", response_model=List[schemas.EnrollmentResponse])
def list_enrollments(db: Session = Depends(get_db)):
    return db.query(models.Enrollment).all()

@router.get("/enrollments/{enrollment_id}", response_model=schemas.EnrollmentResponse)
def get_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    enrollment = db.query(models.Enrollment).filter(models.Enrollment.id == enrollment_id).first()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return enrollment

@router.delete("/enrollments/{enrollment_id}")
def delete_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    enrollment = db.query(models.Enrollment).filter(models.Enrollment.id == enrollment_id).first()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    db.delete(enrollment)
    db.commit()
    return {"detail": "Enrollment deleted"}

# ---- Grades ----
@router.post("/grades", response_model=schemas.GradeResponse)
def create_grade(grade: schemas.GradeCreate, db: Session = Depends(get_db)):
    # Check enrollment exists
    enrollment = db.query(models.Enrollment).filter(models.Enrollment.id == grade.enrollment_id).first()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    # One grade per enrollment
    existing_grade = db.query(models.Grade).filter(models.Grade.enrollment_id == grade.enrollment_id).first()
    if existing_grade:
        raise HTTPException(status_code=400, detail="Grade already exists for this enrollment")
    letter = calculate_letter_grade(grade.score)
    db_grade = models.Grade(enrollment_id=grade.enrollment_id, score=grade.score, letter_grade=letter, graded_at=datetime.utcnow())
    db.add(db_grade)
    db.commit()
    db.refresh(db_grade)
    return db_grade

@router.get("/grades", response_model=List[schemas.GradeResponse])
def list_grades(db: Session = Depends(get_db)):
    return db.query(models.Grade).all()

@router.get("/grades/{grade_id}", response_model=schemas.GradeResponse)
def get_grade(grade_id: int, db: Session = Depends(get_db)):
    grade = db.query(models.Grade).filter(models.Grade.id == grade_id).first()
    if not grade:
        raise HTTPException(status_code=404, detail="Grade not found")
    return grade

@router.put("/grades/{grade_id}", response_model=schemas.GradeResponse)
def update_grade(grade_id: int, grade_update: schemas.GradeCreate, db: Session = Depends(get_db)):
    grade = db.query(models.Grade).filter(models.Grade.id == grade_id).first()
    if not grade:
        raise HTTPException(status_code=404, detail="Grade not found")
    # If enrollment_id changed, check it again
    if grade_update.enrollment_id != grade.enrollment_id:
        enrollment = db.query(models.Enrollment).filter(models.Enrollment.id == grade_update.enrollment_id).first()
        if not enrollment:
            raise HTTPException(status_code=404, detail="Enrollment not found")
        existing = db.query(models.Grade).filter(models.Grade.enrollment_id == grade_update.enrollment_id).first()
        if existing and existing.id != grade_id:
            raise HTTPException(status_code=400, detail="Another grade already exists for that enrollment")
    grade.enrollment_id = grade_update.enrollment_id
    grade.score = grade_update.score
    grade.letter_grade = calculate_letter_grade(grade_update.score)
    grade.graded_at = datetime.utcnow()
    db.commit()
    db.refresh(grade)
    return grade

@router.delete("/grades/{grade_id}")
def delete_grade(grade_id: int, db: Session = Depends(get_db)):
    grade = db.query(models.Grade).filter(models.Grade.id == grade_id).first()
    if not grade:
        raise HTTPException(status_code=404, detail="Grade not found")
    db.delete(grade)
    db.commit()
    return {"detail": "Grade deleted"}

# ---- Assignments ----
@router.post("/assignments", response_model=schemas.AssignmentResponse)
def create_assignment(assignment: schemas.AssignmentCreate, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.id == assignment.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    db_assignment = models.Assignment(**assignment.dict())
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    return db_assignment

@router.get("/assignments", response_model=List[schemas.AssignmentResponse])
def list_assignments(db: Session = Depends(get_db)):
    return db.query(models.Assignment).all()

@router.get("/assignments/{assignment_id}", response_model=schemas.AssignmentResponse)
def get_assignment(assignment_id: int, db: Session = Depends(get_db)):
    assignment = db.query(models.Assignment).filter(models.Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return assignment

@router.put("/assignments/{assignment_id}", response_model=schemas.AssignmentResponse)
def update_assignment(assignment_id: int, assignment_update: schemas.AssignmentCreate, db: Session = Depends(get_db)):
    assignment = db.query(models.Assignment).filter(models.Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    for key, value in assignment_update.dict().items():
        setattr(assignment, key, value)
    db.commit()
    db.refresh(assignment)
    return assignment

@router.delete("/assignments/{assignment_id}")
def delete_assignment(assignment_id: int, db: Session = Depends(get_db)):
    assignment = db.query(models.Assignment).filter(models.Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    db.delete(assignment)
    db.commit()
    return {"detail": "Assignment deleted"}