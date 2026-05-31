from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from . import models, schemas, auth

router = APIRouter()

# ---------- AUTH ----------
@router.post("/token", response_model=schemas.Token)
def login_for_access_token(login: schemas.LoginRequest, db: Session = Depends(auth.get_db)):
    user = auth.authenticate_user(db, login.username, login.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=schemas.UserOut)
def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user

# ---------- USERS ----------
@router.get("/users", response_model=List[schemas.UserOut])
def list_users(db: Session = Depends(auth.get_db), current_user: models.User = Depends(auth.get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can list all users")
    return db.query(models.User).all()

@router.post("/users", response_model=schemas.UserOut, status_code=201)
def create_user(user_in: schemas.UserCreate, db: Session = Depends(auth.get_db), current_user: models.User = Depends(auth.get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can create users")
    # Check uniqueness
    if db.query(models.User).filter(models.User.username == user_in.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    if db.query(models.User).filter(models.User.email == user_in.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")
    hashed_pw = auth.get_password_hash(user_in.password)
    user = models.User(
        username=user_in.username,
        password_hash=hashed_pw,
        role=user_in.role,
        full_name=user_in.full_name,
        email=user_in.email
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.put("/users/{user_id}", response_model=schemas.UserOut)
def update_user(user_id: int, user_in: schemas.UserUpdate, db: Session = Depends(auth.get_db), current_user: models.User = Depends(auth.get_current_user)):
    if current_user.role != "admin" and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Check uniqueness if updating
    if user_in.username and user_in.username != user.username:
        if db.query(models.User).filter(models.User.username == user_in.username).first():
            raise HTTPException(status_code=400, detail="Username already exists")
    if user_in.email and user_in.email != user.email:
        if db.query(models.User).filter(models.User.email == user_in.email).first():
            raise HTTPException(status_code=400, detail="Email already exists")
    for var, value in vars(user_in).items():
        if value is not None:
            if var == "password":
                setattr(user, "password_hash", auth.get_password_hash(value))
            else:
                setattr(user, var, value)
    db.commit()
    db.refresh(user)
    return user

@router.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(auth.get_db), current_user: models.User = Depends(auth.get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can delete users")
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return

# ---------- DEPARTMENTS ----------
@router.get("/departments", response_model=List[schemas.DepartmentOut])
def list_departments(db: Session = Depends(auth.get_db), current_user: models.User = Depends(auth.get_current_user)):
    return db.query(models.Department).all()

@router.post("/departments", response_model=schemas.DepartmentOut, status_code=201)
def create_department(dep_in: schemas.DepartmentCreate, db: Session = Depends(auth.get_db), current_user: models.User = Depends(auth.get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can create departments")
    if db.query(models.Department).filter(models.Department.code == dep_in.code).first():
        raise HTTPException(status_code=400, detail="Department code already exists")
    if db.query(models.Department).filter(models.Department.name == dep_in.name).first():
        raise HTTPException(status_code=400, detail="Department name already exists")
    dep = models.Department(**dep_in.dict())
    db.add(dep)
    db.commit()
    db.refresh(dep)
    return dep

@router.put("/departments/{dep_id}", response_model=schemas.DepartmentOut)
def update_department(dep_id: int, dep_in: schemas.DepartmentCreate, db: Session = Depends(auth.get_db), current_user: models.User = Depends(auth.get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can update departments")
    dep = db.query(models.Department).filter(models.Department.id == dep_id).first()
    if not dep:
        raise HTTPException(status_code=404, detail="Department not found")
    if db.query(models.Department).filter(models.Department.id != dep_id, models.Department.code == dep_in.code).first():
        raise HTTPException(status_code=400, detail="Code already in use")
    if db.query(models.Department).filter(models.Department.id != dep_id, models.Department.name == dep_in.name).first():
        raise HTTPException(status_code=400, detail="Name already in use")
    dep.name = dep_in.name
    dep.code = dep_in.code
    db.commit()
    db.refresh(dep)
    return dep

@router.delete("/departments/{dep_id}", status_code=204)
def delete_department(dep_id: int, db: Session = Depends(auth.get_db), current_user: models.User = Depends(auth.get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can delete departments")
    dep = db.query(models.Department).filter(models.Department.id == dep_id).first()
    if not dep:
        raise HTTPException(status_code=404, detail="Department not found")
    db.delete(dep)
    db.commit()
    return

# ---------- COURSES ----------
@router.get("/courses", response_model=List[schemas.CourseOut])
def list_courses(
    department_id: Optional[int] = Query(None),
    teacher_id: Optional[int] = Query(None),
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    query = db.query(models.Course)
    if department_id:
        query = query.filter(models.Course.department_id == department_id)
    if teacher_id:
        query = query.filter(models.Course.teacher_id == teacher_id)
    # Teachers should only see their courses unless admin
    if current_user.role == "teacher" and not teacher_id:
        query = query.filter(models.Course.teacher_id == current_user.id)
    return query.all()

@router.post("/courses", response_model=schemas.CourseOut, status_code=201)
def create_course(course_in: schemas.CourseCreate, db: Session = Depends(auth.get_db), current_user: models.User = Depends(auth.get_current_user)):
    # Admin or teacher
    if current_user.role not in ["admin", "teacher"]:
        raise HTTPException(status_code=403, detail="Only teachers and admins can create courses")
    if current_user.role == "teacher":
        # Teacher can only create course for themselves
        if course_in.teacher_id != current_user.id:
            raise HTTPException(status_code=403, detail="You can only assign yourself as instructor")
    # Check department exists
    dep = db.query(models.Department).filter(models.Department.id == course_in.department_id).first()
    if not dep:
        raise HTTPException(status_code=404, detail="Department not found")
    # Teacher must exist
    teacher = db.query(models.User).filter(models.User.id == course_in.teacher_id).first()
    if not teacher or teacher.role != "teacher":
        raise HTTPException(status_code=400, detail="Assigned teacher must exist and have teacher role")
    course = models.Course(**course_in.dict())
    db.add(course)
    db.commit()
    db.refresh(course)
    return course

@router.put("/courses/{course_id}", response_model=schemas.CourseOut)
def update_course(course_id: int, course_in: schemas.CourseUpdate, db: Session = Depends(auth.get_db), current_user: models.User = Depends(auth.get_current_user)):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    if current_user.role != "admin" and (current_user.role != "teacher" or course.teacher_id != current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to update this course")
    update_data = course_in.dict(exclude_unset=True)
    # Handle teacher_id change with role validation
    if "teacher_id" in update_data:
        teacher = db.query(models.User).filter(models.User.id == update_data["teacher_id"]).first()
        if not teacher or teacher.role != "teacher":
            raise HTTPException(status_code=400, detail="Assigned teacher must be a teacher")
    for key, value in update_data.items():
        setattr(course, key, value)
    db.commit()
    db.refresh(course)
    return course

@router.delete("/courses/{course_id}", status_code=204)
def delete_course(course_id: int, db: Session = Depends(auth.get_db), current_user: models.User = Depends(auth.get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can delete courses")
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    db.delete(course)
    db.commit()
    return

# ---------- ENROLLMENTS ----------
@router.get("/enrollments", response_model=List[schemas.EnrollmentOut])
def list_enrollments(
    student_id: Optional[int] = Query(None),
    course_id: Optional[int] = Query(None),
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    query = db.query(models.Enrollment)
    # Role-based filtering
    if current_user.role == "student":
        query = query.filter(models.Enrollment.student_id == current_user.id)
    elif current_user.role == "teacher":
        # Teacher can see enrollments for courses they teach
        query = query.join(models.Course).filter(models.Course.teacher_id == current_user.id)
    # Admin can see all, optionally filter
    if student_id and current_user.role == "admin":
        query = query.filter(models.Enrollment.student_id == student_id)
    if course_id and current_user.role in ["admin", "teacher"]:
        query = query.filter(models.Enrollment.course_id == course_id)
    return query.all()

@router.post("/enrollments", response_model=schemas.EnrollmentOut, status_code=201)
def create_enrollment(
    enrollment_in: schemas.EnrollmentCreate,
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    # Only students can enroll themselves (student_id must be current user)
    if current_user.role != "student":
        raise HTTPException(status_code=403, detail="Only students can enroll")
    if enrollment_in.student_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only enroll yourself")

    # Check student exists and is a student
    student = db.query(models.User).filter(models.User.id == enrollment_in.student_id).first()
    if not student or student.role != "student":
        raise HTTPException(status_code=400, detail="Invalid student")

    course = db.query(models.Course).filter(models.Course.id == enrollment_in.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # Duplicate check
    existing = db.query(models.Enrollment).filter(
        models.Enrollment.student_id == enrollment_in.student_id,
        models.Enrollment.course_id == enrollment_in.course_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already enrolled in this course")

    # Capacity check
    enrolled_count = db.query(models.Enrollment).filter(models.Enrollment.course_id == course.id).count()
    if enrolled_count >= course.capacity:
        raise HTTPException(status_code=400, detail="Course has reached maximum capacity")

    # Credit limit check: sum of credits of all courses student is enrolled in (+ this one)
    current_credits = db.query(models.Course.credits).join(models.Enrollment).filter(
        models.Enrollment.student_id == student.id
    ).all()
    total_credits = sum(c[0] for c in current_credits) + course.credits
    if total_credits > 30:
        raise HTTPException(status_code=400, detail=f"Enrolling would exceed 30 credit limit (current: {total_credits - course.credits}, adding {course.credits})")

    enrollment = models.Enrollment(student_id=student.id, course_id=course.id)
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    return enrollment

@router.delete("/enrollments/{enrollment_id}", status_code=204)
def delete_enrollment(enrollment_id: int, db: Session = Depends(auth.get_db), current_user: models.User = Depends(auth.get_current_user)):
    enrollment = db.query(models.Enrollment).filter(models.Enrollment.id == enrollment_id).first()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    # Students can drop their own enrollment; admins can drop any
    if current_user.role != "admin" and enrollment.student_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    db.delete(enrollment)
    db.commit()
    return

# ---------- GRADES ----------
@router.get("/grades", response_model=List[schemas.GradeOut])
def list_grades(
    enrollment_id: Optional[int] = Query(None),
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    query = db.query(models.Grade)
    if current_user.role == "student":
        query = query.join(models.Enrollment).filter(models.Enrollment.student_id == current_user.id)
    elif current_user.role == "teacher":
        query = query.join(models.Enrollment).join(models.Course).filter(models.Course.teacher_id == current_user.id)
    if enrollment_id:
        query = query.filter(models.Grade.enrollment_id == enrollment_id)
    return query.all()

@router.post("/grades", response_model=schemas.GradeOut, status_code=201)
def create_grade(
    grade_in: schemas.GradeCreate,
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can assign grades")
    enrollment = db.query(models.Enrollment).filter(models.Enrollment.id == grade_in.enrollment_id).first()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    # Ensure teacher is the instructor of the course of this enrollment
    course = db.query(models.Course).filter(models.Course.id == enrollment.course_id).first()
    if course.teacher_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not the instructor of this course")
    # One grade per enrollment
    existing = db.query(models.Grade).filter(models.Grade.enrollment_id == grade_in.enrollment_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Grade already exists for this enrollment")
    # Calculate letter grade (optional)
    letter = None
    score = grade_in.score
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
    grade = models.Grade(
        enrollment_id=grade_in.enrollment_id,
        score=score,
        letter_grade=letter,
        graded_at=datetime.utcnow()
    )
    db.add(grade)
    db.commit()
    db.refresh(grade)
    return grade

@router.put("/grades/{grade_id}", response_model=schemas.GradeOut)
def update_grade(grade_id: int, grade_in: schemas.GradeUpdate, db: Session = Depends(auth.get_db), current_user: models.User = Depends(auth.get_current_user)):
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can update grades")
    grade = db.query(models.Grade).filter(models.Grade.id == grade_id).first()
    if not grade:
        raise HTTPException(status_code=404, detail="Grade not found")
    enrollment = grade.enrollment
    course = enrollment.course
    if course.teacher_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not the instructor of this course")
    if grade_in.score is not None:
        grade.score = grade_in.score
        if grade.score >= 90:
            grade.letter_grade = "A"
        elif grade.score >= 80:
            grade.letter_grade = "B"
        elif grade.score >= 70:
            grade.letter_grade = "C"
        elif grade.score >= 60:
            grade.letter_grade = "D"
        else:
            grade.letter_grade = "F"
        grade.graded_at = datetime.utcnow()
    db.commit()
    db.refresh(grade)
    return grade

# ---------- ASSIGNMENTS ----------
@router.get("/assignments", response_model=List[schemas.AssignmentOut])
def list_assignments(
    course_id: Optional[int] = Query(None),
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    query = db.query(models.Assignment)
    if current_user.role == "student":
        # student can see assignments of courses they're enrolled in
        enrolled_course_ids = db.query(models.Enrollment.course_id).filter(models.Enrollment.student_id == current_user.id).subquery()
        query = query.filter(models.Assignment.course_id.in_(enrolled_course_ids))
    elif current_user.role == "teacher":
        # teacher sees assignments of courses they teach
        taught_course_ids = db.query(models.Course.id).filter(models.Course.teacher_id == current_user.id).subquery()
        query = query.filter(models.Assignment.course_id.in_(taught_course_ids))
    if course_id:
        query = query.filter(models.Assignment.course_id == course_id)
    return query.all()

@router.post("/assignments", response_model=schemas.AssignmentOut, status_code=201)
def create_assignment(
    assignment_in: schemas.AssignmentCreate,
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can create assignments")
    # Check course belongs to this teacher
    course = db.query(models.Course).filter(models.Course.id == assignment_in.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    if course.teacher_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not the instructor of this course")
    assignment = models.Assignment(**assignment_in.dict())
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    return assignment

@router.put("/assignments/{assign_id}", response_model=schemas.AssignmentOut)
def update_assignment(assign_id: int, assignment_in: schemas.AssignmentUpdate, db: Session = Depends(auth.get_db), current_user: models.User = Depends(auth.get_current_user)):
    assignment = db.query(models.Assignment).filter(models.Assignment.id == assign_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    course = assignment.course
    if course.teacher_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    update_data = assignment_in.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(assignment, key, value)
    db.commit()
    db.refresh(assignment)
    return assignment

@router.delete("/assignments/{assign_id}", status_code=204)
def delete_assignment(assign_id: int, db: Session = Depends(auth.get_db), current_user: models.User = Depends(auth.get_current_user)):
    assignment = db.query(models.Assignment).filter(models.Assignment.id == assign_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    course = assignment.course
    if course.teacher_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    db.delete(assignment)
    db.commit()
    return

# ---------- SUBMISSIONS ----------
@router.get("/submissions", response_model=List[schemas.SubmissionOut])
def list_submissions(
    assignment_id: Optional[int] = Query(None),
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    query = db.query(models.Submission)
    if current_user.role == "student":
        query = query.filter(models.Submission.student_id == current_user.id)
    elif current_user.role == "teacher":
        # submissions for assignments of courses they teach
        teacher_courses = db.query(models.Course.id).filter(models.Course.teacher_id == current_user.id).subquery()
        query = query.join(models.Assignment).filter(models.Assignment.course_id.in_(teacher_courses))
    if assignment_id:
        query = query.filter(models.Submission.assignment_id == assignment_id)
    return query.all()

@router.post("/submissions", response_model=schemas.SubmissionOut, status_code=201)
def create_submission(
    submission_in: schemas.SubmissionCreate,
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    if current_user.role != "student":
        raise HTTPException(status_code=403, detail="Only students can submit assignments")
    # Check assignment exists
    assignment = db.query(models.Assignment).filter(models.Assignment.id == submission_in.assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    # Check student is enrolled in corresponding course
    enrollment = db.query(models.Enrollment).filter(
        models.Enrollment.student_id == current_user.id,
        models.Enrollment.course_id == assignment.course_id
    ).first()
    if not enrollment:
        raise HTTPException(status_code=403, detail="You are not enrolled in this course")
    # Duplicate check (one submission per assignment per student)
    existing = db.query(models.Submission).filter(
        models.Submission.assignment_id == submission_in.assignment_id,
        models.Submission.student_id == current_user.id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="You have already submitted for this assignment")

    # Determine if late
    now = datetime.utcnow()
    is_late = now > assignment.due_date

    submission = models.Submission(
        assignment_id=assignment.id,
        student_id=current_user.id,
        content=submission_in.content,
        submitted_at=now,
        is_late=is_late
    )
    db.add(submission)
    db.commit()
    db.refresh(submission)
    return submission

# Note: No update or delete for submissions for simplicity; can be added if needed.