from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from database import SessionLocal
import models, schemas

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter()

# ---------- Users ----------
@router.get("/users/", response_model=List[schemas.UserResponse])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.User).offset(skip).limit(limit).all()

@router.get("/users/{user_id}", response_model=schemas.UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/users/", response_model=schemas.UserResponse, status_code=201)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if db.query(models.User).filter(
        (models.User.username == user.username) | (models.User.email == user.email)
    ).first():
        raise HTTPException(status_code=400, detail="Username or email already exists")
    db_user = models.User(
        username=user.username,
        password_hash=user.password,  # In real app, hash it
        role=user.role,
        full_name=user.full_name,
        email=user.email
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.put("/users/{user_id}", response_model=schemas.UserResponse)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).get(user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    update_data = user.dict(exclude_unset=True)
    if 'password' in update_data and update_data['password']:
        update_data['password_hash'] = update_data.pop('password')
    for k, v in update_data.items():
        setattr(db_user, k, v)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).get(user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return

# ---------- Departments ----------
@router.get("/departments/", response_model=List[schemas.DepartmentResponse])
def read_departments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Department).offset(skip).limit(limit).all()

@router.post("/departments/", response_model=schemas.DepartmentResponse, status_code=201)
def create_department(dept: schemas.DepartmentCreate, db: Session = Depends(get_db)):
    if db.query(models.Department).filter(models.Department.code == dept.code).first():
        raise HTTPException(status_code=400, detail="Department code already exists")
    db_dept = models.Department(**dept.dict())
    db.add(db_dept)
    db.commit()
    db.refresh(db_dept)
    return db_dept

@router.get("/departments/{dept_id}", response_model=schemas.DepartmentResponse)
def read_department(dept_id: int, db: Session = Depends(get_db)):
    dept = db.query(models.Department).get(dept_id)
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")
    return dept

@router.put("/departments/{dept_id}", response_model=schemas.DepartmentResponse)
def update_department(dept_id: int, dept: schemas.DepartmentCreate, db: Session = Depends(get_db)):
    db_dept = db.query(models.Department).get(dept_id)
    if not db_dept:
        raise HTTPException(status_code=404, detail="Department not found")
    for k, v in dept.dict().items():
        setattr(db_dept, k, v)
    db.commit()
    db.refresh(db_dept)
    return db_dept

@router.delete("/departments/{dept_id}", status_code=204)
def delete_department(dept_id: int, db: Session = Depends(get_db)):
    db_dept = db.query(models.Department).get(dept_id)
    if not db_dept:
        raise HTTPException(status_code=404, detail="Department not found")
    db.delete(db_dept)
    db.commit()
    return

# ---------- Courses ----------
@router.get("/courses/", response_model=List[schemas.CourseResponse])
def read_courses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Course).offset(skip).limit(limit).all()

@router.get("/courses/{course_id}", response_model=schemas.CourseResponse)
def read_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(models.Course).get(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.post("/courses/", response_model=schemas.CourseResponse, status_code=201)
def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    if course.instructor_id:
        instr = db.query(models.User).get(course.instructor_id)
        if not instr or instr.role != "teacher":
            raise HTTPException(status_code=400, detail="Instructor must be a teacher")
    if not db.query(models.Department).get(course.department_id):
        raise HTTPException(status_code=400, detail="Department not found")
    db_course = models.Course(**course.dict())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

@router.put("/courses/{course_id}", response_model=schemas.CourseResponse)
def update_course(course_id: int, course: schemas.CourseUpdate, db: Session = Depends(get_db)):
    db_course = db.query(models.Course).get(course_id)
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    if course.instructor_id:
        instr = db.query(models.User).get(course.instructor_id)
        if not instr or instr.role != "teacher":
            raise HTTPException(status_code=400, detail="Instructor must be a teacher")
    for k, v in course.dict().items():
        setattr(db_course, k, v)
    db.commit()
    db.refresh(db_course)
    return db_course

@router.delete("/courses/{course_id}", status_code=204)
def delete_course(course_id: int, db: Session = Depends(get_db)):
    db_course = db.query(models.Course).get(course_id)
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    db.delete(db_course)
    db.commit()
    return

# ---------- Enrollments ----------
@router.get("/enrollments/", response_model=List[schemas.EnrollmentResponse])
def read_enrollments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Enrollment).offset(skip).limit(limit).all()

@router.post("/enrollments/", response_model=schemas.EnrollmentResponse, status_code=201)
def create_enrollment(enr: schemas.EnrollmentCreate, db: Session = Depends(get_db)):
    student = db.query(models.User).get(enr.student_id)
    if not student or student.role != "student":
        raise HTTPException(status_code=400, detail="Only students can enroll")
    course = db.query(models.Course).get(enr.course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    # capacity check
    enrolled_count = db.query(models.Enrollment).filter(models.Enrollment.course_id == course.id).count()
    if enrolled_count >= course.capacity:
        raise HTTPException(status_code=400, detail="Course is full")
    # duplicate check enforced by DB unique constraint, but we can explicitly check
    exists = db.query(models.Enrollment).filter(
        models.Enrollment.student_id == student.id,
        models.Enrollment.course_id == course.id
    ).first()
    if exists:
        raise HTTPException(status_code=400, detail="Already enrolled")
    # credit limit
    current_credits = db.query(models.Course.credits).join(models.Enrollment).filter(
        models.Enrollment.student_id == student.id
    ).all()
    total_credits = sum(c[0] for c in current_credits) + course.credits
    if total_credits > 30:
        raise HTTPException(status_code=400, detail="Credit limit exceeded (max 30)")
    db_enr = models.Enrollment(student_id=student.id, course_id=course.id)
    db.add(db_enr)
    db.commit()
    db.refresh(db_enr)
    return db_enr

@router.delete("/enrollments/{enrollment_id}", status_code=204)
def delete_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    enr = db.query(models.Enrollment).get(enrollment_id)
    if not enr:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    db.delete(enr)
    db.commit()
    return

# ---------- Grades ----------
@router.get("/grades/", response_model=List[schemas.GradeResponse])
def read_grades(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Grade).offset(skip).limit(limit).all()

@router.get("/grades/{grade_id}", response_model=schemas.GradeResponse)
def read_grade(grade_id: int, db: Session = Depends(get_db)):
    grade = db.query(models.Grade).get(grade_id)
    if not grade:
        raise HTTPException(status_code=404, detail="Grade not found")
    return grade

@router.post("/grades/", response_model=schemas.GradeResponse, status_code=201)
def create_grade(grade: schemas.GradeCreate, db: Session = Depends(get_db)):
    enrollment = db.query(models.Enrollment).get(grade.enrollment_id)
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    if db.query(models.Grade).filter(models.Grade.enrollment_id == grade.enrollment_id).first():
        raise HTTPException(status_code=400, detail="Grade already assigned")
    score = grade.score
    if score >= 90:
        letter = "A"
    elif score >= 80:
        letter = "B"
    elif score >= 70:
        letter = "C"
    elif score >= 60:
        letter = "D"
    else:
        letter = "F"
    db_grade = models.Grade(enrollment_id=grade.enrollment_id, score=score, letter_grade=letter)
    db.add(db_grade)
    db.commit()
    db.refresh(db_grade)
    return db_grade

@router.put("/grades/{grade_id}", response_model=schemas.GradeResponse)
def update_grade(grade_id: int, grade: schemas.GradeUpdate, db: Session = Depends(get_db)):
    db_grade = db.query(models.Grade).get(grade_id)
    if not db_grade:
        raise HTTPException(status_code=404, detail="Grade not found")
    score = grade.score
    if grade.letter_grade:
        letter = grade.letter_grade
    else:
        if score >= 90: letter = "A"
        elif score >= 80: letter = "B"
        elif score >= 70: letter = "C"
        elif score >= 60: letter = "D"
        else: letter = "F"
    db_grade.score = score
    db_grade.letter_grade = letter
    db_grade.graded_at = datetime.utcnow()
    db.commit()
    db.refresh(db_grade)
    return db_grade

@router.delete("/grades/{grade_id}", status_code=204)
def delete_grade(grade_id: int, db: Session = Depends(get_db)):
    db_grade = db.query(models.Grade).get(grade_id)
    if not db_grade:
        raise HTTPException(status_code=404, detail="Grade not found")
    db.delete(db_grade)
    db.commit()
    return

# ---------- Assignments ----------
@router.get("/assignments/", response_model=List[schemas.AssignmentResponse])
def read_assignments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Assignment).offset(skip).limit(limit).all()

@router.get("/assignments/{assignment_id}", response_model=schemas.AssignmentResponse)
def read_assignment(assignment_id: int, db: Session = Depends(get_db)):
    assignment = db.query(models.Assignment).get(assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return assignment

@router.post("/assignments/", response_model=schemas.AssignmentResponse, status_code=201)
def create_assignment(assignment: schemas.AssignmentCreate, db: Session = Depends(get_db)):
    if not db.query(models.Course).get(assignment.course_id):
        raise HTTPException(status_code=404, detail="Course not found")
    if assignment.due_date <= datetime.utcnow():
        raise HTTPException(status_code=400, detail="Due date must be in the future")
    db_assignment = models.Assignment(**assignment.dict())
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    return db_assignment

@router.put("/assignments/{assignment_id}", response_model=schemas.AssignmentResponse)
def update_assignment(assignment_id: int, assignment: schemas.AssignmentUpdate, db: Session = Depends(get_db)):
    db_assignment = db.query(models.Assignment).get(assignment_id)
    if not db_assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    if assignment.due_date <= datetime.utcnow():
        raise HTTPException(status_code=400, detail="Due date must be in the future")
    for k, v in assignment.dict().items():
        setattr(db_assignment, k, v)
    db.commit()
    db.refresh(db_assignment)
    return db_assignment

@router.delete("/assignments/{assignment_id}", status_code=204)
def delete_assignment(assignment_id: int, db: Session = Depends(get_db)):
    db_assignment = db.query(models.Assignment).get(assignment_id)
    if not db_assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    db.delete(db_assignment)
    db.commit()
    return