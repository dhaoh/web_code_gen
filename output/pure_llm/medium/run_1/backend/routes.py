from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal, engine
import models, schemas
from datetime import datetime

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Helper: compute letter grade
def compute_letter_grade(score: float) -> str:
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"

# -------------------
# Auth (simple plaintext)
# -------------------
@router.post("/login", response_model=schemas.UserResponse)
def login(req: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == req.username).first()
    if not user or user.password_hash != req.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user

# -------------------
# Users CRUD
# -------------------
@router.get("/users", response_model=List[schemas.UserResponse])
def list_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

@router.post("/users", response_model=schemas.UserResponse, status_code=201)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # check unique username/email
    if db.query(models.User).filter(models.User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")
    db_user = models.User(
        username=user.username,
        password_hash=user.password,  # storing plain for demo
        role=user.role,
        full_name=user.full_name,
        email=user.email
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/users/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/users/{user_id}", response_model=schemas.UserResponse)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.username is not None:
        db_user.username = user.username
    if user.password is not None:
        db_user.password_hash = user.password
    if user.role is not None:
        db_user.role = user.role
    if user.full_name is not None:
        db_user.full_name = user.full_name
    if user.email is not None:
        db_user.email = user.email
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return

# -------------------
# Departments CRUD
# -------------------
@router.get("/departments", response_model=List[schemas.DepartmentResponse])
def list_departments(db: Session = Depends(get_db)):
    return db.query(models.Department).all()

@router.post("/departments", response_model=schemas.DepartmentResponse, status_code=201)
def create_department(dep: schemas.DepartmentCreate, db: Session = Depends(get_db)):
    if db.query(models.Department).filter(models.Department.code == dep.code).first():
        raise HTTPException(status_code=400, detail="Department code already exists")
    if db.query(models.Department).filter(models.Department.name == dep.name).first():
        raise HTTPException(status_code=400, detail="Department name already exists")
    db_dep = models.Department(**dep.dict())
    db.add(db_dep)
    db.commit()
    db.refresh(db_dep)
    return db_dep

@router.get("/departments/{dep_id}", response_model=schemas.DepartmentResponse)
def get_department(dep_id: int, db: Session = Depends(get_db)):
    dep = db.query(models.Department).filter(models.Department.id == dep_id).first()
    if not dep:
        raise HTTPException(status_code=404, detail="Department not found")
    return dep

@router.put("/departments/{dep_id}", response_model=schemas.DepartmentResponse)
def update_department(dep_id: int, dep: schemas.DepartmentCreate, db: Session = Depends(get_db)):
    db_dep = db.query(models.Department).filter(models.Department.id == dep_id).first()
    if not db_dep:
        raise HTTPException(status_code=404, detail="Department not found")
    db_dep.name = dep.name
    db_dep.code = dep.code
    db.commit()
    db.refresh(db_dep)
    return db_dep

@router.delete("/departments/{dep_id}", status_code=204)
def delete_department(dep_id: int, db: Session = Depends(get_db)):
    db_dep = db.query(models.Department).filter(models.Department.id == dep_id).first()
    if not db_dep:
        raise HTTPException(status_code=404, detail="Department not found")
    db.delete(db_dep)
    db.commit()
    return

# -------------------
# Courses CRUD
# -------------------
@router.get("/courses", response_model=List[schemas.CourseResponse])
def list_courses(db: Session = Depends(get_db)):
    return db.query(models.Course).all()

@router.post("/courses", response_model=schemas.CourseResponse, status_code=201)
def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    # Check teacher exists and has role teacher
    teacher = db.query(models.User).filter(models.User.id == course.teacher_id).first()
    if not teacher or teacher.role != "teacher":
        raise HTTPException(status_code=400, detail="Teacher must be a user with role 'teacher'")
    dep = db.query(models.Department).filter(models.Department.id == course.department_id).first()
    if not dep:
        raise HTTPException(status_code=400, detail="Department not found")
    db_course = models.Course(**course.dict())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

@router.get("/courses/{course_id}", response_model=schemas.CourseResponse)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.put("/courses/{course_id}", response_model=schemas.CourseResponse)
def update_course(course_id: int, course: schemas.CourseUpdate, db: Session = Depends(get_db)):
    db_course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    for key, value in course.dict(exclude_unset=True).items():
        setattr(db_course, key, value)
    db.commit()
    db.refresh(db_course)
    return db_course

@router.delete("/courses/{course_id}", status_code=204)
def delete_course(course_id: int, db: Session = Depends(get_db)):
    db_course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    db.delete(db_course)
    db.commit()
    return

# -------------------
# Enrollments (with business rules)
# -------------------
@router.post("/enrollments", response_model=schemas.EnrollmentResponse, status_code=201)
def create_enrollment(enrollment: schemas.EnrollmentCreate, db: Session = Depends(get_db)):
    # student_role_check
    student = db.query(models.User).filter(models.User.id == enrollment.student_id).first()
    if not student or student.role != "student":
        raise HTTPException(status_code=400, detail="Only students can enroll")
    course = db.query(models.Course).filter(models.Course.id == enrollment.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # duplicate_enrollment
    existing = db.query(models.Enrollment).filter(
        models.Enrollment.student_id == enrollment.student_id,
        models.Enrollment.course_id == enrollment.course_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already enrolled in this course")

    # capacity_check
    enrolled_count = db.query(models.Enrollment).filter(models.Enrollment.course_id == enrollment.course_id).count()
    if enrolled_count >= course.capacity:
        raise HTTPException(status_code=400, detail="Course is full")

    # credit_limit
    current_credits = db.query(models.Course.credits).join(models.Enrollment).filter(
        models.Enrollment.student_id == enrollment.student_id
    ).all()
    total_credits = sum(c[0] for c in current_credits) + course.credits
    if total_credits > 30:
        raise HTTPException(status_code=400, detail="Credit limit exceeded (max 30)")

    db_enrollment = models.Enrollment(
        student_id=enrollment.student_id,
        course_id=enrollment.course_id,
        enrolled_at=datetime.utcnow()
    )
    db.add(db_enrollment)
    db.commit()
    db.refresh(db_enrollment)
    return db_enrollment

@router.get("/enrollments", response_model=List[schemas.EnrollmentResponse])
def list_enrollments(db: Session = Depends(get_db)):
    return db.query(models.Enrollment).all()

@router.get("/enrollments/{enrollment_id}", response_model=schemas.EnrollmentResponse)
def get_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    enroll = db.query(models.Enrollment).filter(models.Enrollment.id == enrollment_id).first()
    if not enroll:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return enroll

@router.delete("/enrollments/{enrollment_id}", status_code=204)
def delete_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    enroll = db.query(models.Enrollment).filter(models.Enrollment.id == enrollment_id).first()
    if not enroll:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    db.delete(enroll)
    db.commit()
    return

# -------------------
# Grades (assign grade to enrollment)
# -------------------
@router.post("/grades", response_model=schemas.GradeResponse, status_code=201)
def create_grade(grade: schemas.GradeCreate, db: Session = Depends(get_db)):
    enrollment = db.query(models.Enrollment).filter(models.Enrollment.id == grade.enrollment_id).first()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    existing_grade = db.query(models.Grade).filter(models.Grade.enrollment_id == grade.enrollment_id).first()
    if existing_grade:
        raise HTTPException(status_code=400, detail="Grade already assigned for this enrollment")
    letter = grade.letter_grade or compute_letter_grade(grade.score)
    db_grade = models.Grade(
        enrollment_id=grade.enrollment_id,
        score=grade.score,
        letter_grade=letter,
        graded_at=datetime.utcnow()
    )
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
def update_grade(grade_id: int, grade: schemas.GradeCreate, db: Session = Depends(get_db)):
    db_grade = db.query(models.Grade).filter(models.Grade.id == grade_id).first()
    if not db_grade:
        raise HTTPException(status_code=404, detail="Grade not found")
    db_grade.score = grade.score
    db_grade.letter_grade = grade.letter_grade or compute_letter_grade(grade.score)
    db_grade.graded_at = datetime.utcnow()
    db.commit()
    db.refresh(db_grade)
    return db_grade

# -------------------
# Assignments
# -------------------
@router.post("/assignments", response_model=schemas.AssignmentResponse, status_code=201)
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
def update_assignment(assignment_id: int, assignment: schemas.AssignmentCreate, db: Session = Depends(get_db)):
    db_assignment = db.query(models.Assignment).filter(models.Assignment.id == assignment_id).first()
    if not db_assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    for key, value in assignment.dict().items():
        setattr(db_assignment, key, value)
    db.commit()
    db.refresh(db_assignment)
    return db_assignment

@router.delete("/assignments/{assignment_id}", status_code=204)
def delete_assignment(assignment_id: int, db: Session = Depends(get_db)):
    db_assignment = db.query(models.Assignment).filter(models.Assignment.id == assignment_id).first()
    if not db_assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    db.delete(db_assignment)
    db.commit()
    return

# -------------------
# Submissions (student submits assignment)
# -------------------
@router.post("/assignments/{assignment_id}/submissions", response_model=schemas.SubmissionResponse, status_code=201)
def submit_assignment(assignment_id: int, sub: schemas.SubmissionCreate, db: Session = Depends(get_db)):
    assignment = db.query(models.Assignment).filter(models.Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    student = db.query(models.User).filter(models.User.id == sub.student_id).first()
    if not student or student.role != "student":
        raise HTTPException(status_code=400, detail="Only students can submit assignments")
    submitted_at = sub.submitted_at or datetime.utcnow()
    is_late = submitted_at > assignment.due_date if submitted_at else False
    db_sub = models.Submission(
        assignment_id=assignment_id,
        student_id=sub.student_id,
        content=sub.content,
        submitted_at=submitted_at,
        is_late=is_late
    )
    db.add(db_sub)
    db.commit()
    db.refresh(db_sub)
    return db_sub

@router.get("/assignments/{assignment_id}/submissions", response_model=List[schemas.SubmissionResponse])
def list_submissions(assignment_id: int, db: Session = Depends(get_db)):
    assignment = db.query(models.Assignment).filter(models.Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return db.query(models.Submission).filter(models.Submission.assignment_id == assignment_id).all()

@router.get("/submissions/{submission_id}", response_model=schemas.SubmissionResponse)
def get_submission(submission_id: int, db: Session = Depends(get_db)):
    sub = db.query(models.Submission).filter(models.Submission.id == submission_id).first()
    if not sub:
        raise HTTPException(status_code=404, detail="Submission not found")
    return sub