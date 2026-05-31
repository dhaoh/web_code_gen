from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from .database import SessionLocal
from . import models, schemas, auth
from typing import List, Optional
from datetime import datetime

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------- Helper functions ----------
def check_schedule_conflict(db: Session, student_id: int, new_course: models.Course):
    # Get all currently enrolled courses for student (enrolled status)
    enrolled = db.query(models.Enrollment).filter(
        models.Enrollment.student_id == student_id,
        models.Enrollment.status == "enrolled"
    ).all()
    # Schedules of new course
    new_schedules = new_course.schedules
    for enr in enrolled:
        other_course = enr.course
        other_schedules = other_course.schedules
        for ns in new_schedules:
            for os in other_schedules:
                if ns.day_of_week == os.day_of_week:
                    if ns.start_time < os.end_time and os.start_time < ns.end_time:
                        return True
    return False

def check_credit_limit(db: Session, student_id: int, new_course: models.Course):
    # Sum credits of all enrolled courses in same semester
    same_semester_courses = db.query(models.Enrollment).join(models.Course).filter(
        models.Enrollment.student_id == student_id,
        models.Enrollment.status == "enrolled",
        models.Course.semester == new_course.semester
    ).all()
    total_credits = sum(e.course.credits for e in same_semester_courses)
    return (total_credits + new_course.credits) > 30

# ---------- Auth ----------
@router.post("/auth/login", response_model=schemas.Token)
def login(login_data: schemas.Login, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == login_data.username).first()
    if not user or not auth.verify_password(login_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    token = auth.create_access_token(data={"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/users/me", response_model=schemas.UserOut)
def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user

# ---------- Users ----------
@router.get("/users", response_model=List[schemas.UserOut])
def get_users(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    return db.query(models.User).all()

@router.post("/users", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed = auth.get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        password_hash=hashed,
        role=user.role,
        full_name=user.full_name,
        email=user.email,
        major_id=user.major_id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.put("/users/{user_id}", response_model=schemas.UserOut)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    update_data = user.dict(exclude_unset=True)
    if "password" in update_data:
        raise HTTPException(status_code=400, detail="Use dedicated endpoint to change password")
    for key, value in update_data.items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"ok": True}

# ---------- Departments ----------
@router.get("/departments", response_model=List[schemas.DepartmentOut])
def get_departments(db: Session = Depends(get_db)):
    return db.query(models.Department).all()

@router.post("/departments", response_model=schemas.DepartmentOut)
def create_department(dep: schemas.DepartmentCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_dep = models.Department(**dep.dict())
    db.add(db_dep)
    db.commit()
    db.refresh(db_dep)
    return db_dep

@router.put("/departments/{dep_id}", response_model=schemas.DepartmentOut)
def update_department(dep_id: int, dep: schemas.DepartmentUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_dep = db.query(models.Department).filter(models.Department.id == dep_id).first()
    if not db_dep:
        raise HTTPException(status_code=404, detail="Department not found")
    update_data = dep.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_dep, key, value)
    db.commit()
    db.refresh(db_dep)
    return db_dep

@router.delete("/departments/{dep_id}")
def delete_department(dep_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_dep = db.query(models.Department).filter(models.Department.id == dep_id).first()
    if not db_dep:
        raise HTTPException(status_code=404, detail="Department not found")
    db.delete(db_dep)
    db.commit()
    return {"ok": True}

# ---------- Majors ----------
@router.get("/majors", response_model=List[schemas.MajorOut])
def get_majors(db: Session = Depends(get_db)):
    return db.query(models.Major).all()

@router.post("/majors", response_model=schemas.MajorOut)
def create_major(major: schemas.MajorCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_major = models.Major(**major.dict())
    db.add(db_major)
    db.commit()
    db.refresh(db_major)
    return db_major

@router.put("/majors/{major_id}", response_model=schemas.MajorOut)
def update_major(major_id: int, major: schemas.MajorUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_major = db.query(models.Major).filter(models.Major.id == major_id).first()
    if not db_major:
        raise HTTPException(status_code=404, detail="Major not found")
    update_data = major.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_major, key, value)
    db.commit()
    db.refresh(db_major)
    return db_major

@router.delete("/majors/{major_id}")
def delete_major(major_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_major = db.query(models.Major).filter(models.Major.id == major_id).first()
    if not db_major:
        raise HTTPException(status_code=404, detail="Major not found")
    db.delete(db_major)
    db.commit()
    return {"ok": True}

# ---------- Courses ----------
@router.get("/courses", response_model=List[schemas.CourseOut])
def get_courses(db: Session = Depends(get_db)):
    return db.query(models.Course).all()

@router.post("/courses", response_model=schemas.CourseOut)
def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    # Only department head of the department can create course
    if current_user.role != "department_head":
        raise HTTPException(status_code=403, detail="Only department heads can create courses")
    dept = db.query(models.Department).filter(models.Department.id == course.department_id).first()
    if dept and dept.head_user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not the head of this department")
    db_course = models.Course(**course.dict())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

@router.put("/courses/{course_id}", response_model=schemas.CourseOut)
def update_course(course_id: int, course: schemas.CourseUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    # Department head of the department can update
    if current_user.role != "department_head" or db_course.department.head_user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only the department head can update this course")
    update_data = course.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_course, key, value)
    db.commit()
    db.refresh(db_course)
    return db_course

@router.delete("/courses/{course_id}")
def delete_course(course_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    if current_user.role != "department_head" or db_course.department.head_user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only the department head can delete this course")
    db.delete(db_course)
    db.commit()
    return {"ok": True}

# ---------- Prerequisites ----------
@router.get("/prerequisites", response_model=List[schemas.PrerequisiteOut])
def get_prerequisites(db: Session = Depends(get_db)):
    return db.query(models.Prerequisite).all()

@router.post("/prerequisites", response_model=schemas.PrerequisiteOut)
def create_prerequisite(preq: schemas.PrerequisiteCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    # Only department head of the course's department can add prerequisites
    course = db.query(models.Course).filter(models.Course.id == preq.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    if current_user.role != "department_head" or course.department.head_user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    db_preq = models.Prerequisite(**preq.dict())
    db.add(db_preq)
    db.commit()
    db.refresh(db_preq)
    return db_preq

@router.put("/prerequisites/{preq_id}", response_model=schemas.PrerequisiteOut)
def update_prerequisite(preq_id: int, preq: schemas.PrerequisiteUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_preq = db.query(models.Prerequisite).filter(models.Prerequisite.id == preq_id).first()
    if not db_preq:
        raise HTTPException(status_code=404, detail="Prerequisite not found")
    course = db_preq.course
    if current_user.role != "department_head" or course.department.head_user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    update_data = preq.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_preq, key, value)
    db.commit()
    db.refresh(db_preq)
    return db_preq

@router.delete("/prerequisites/{preq_id}")
def delete_prerequisite(preq_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_preq = db.query(models.Prerequisite).filter(models.Prerequisite.id == preq_id).first()
    if not db_preq:
        raise HTTPException(status_code=404, detail="Prerequisite not found")
    course = db_preq.course
    if current_user.role != "department_head" or course.department.head_user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    db.delete(db_preq)
    db.commit()
    return {"ok": True}

# ---------- Classrooms ----------
@router.get("/classrooms", response_model=List[schemas.ClassroomOut])
def get_classrooms(db: Session = Depends(get_db)):
    return db.query(models.Classroom).all()

@router.post("/classrooms", response_model=schemas.ClassroomOut)
def create_classroom(room: schemas.ClassroomCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_room = models.Classroom(**room.dict())
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room

@router.put("/classrooms/{room_id}", response_model=schemas.ClassroomOut)
def update_classroom(room_id: int, room: schemas.ClassroomUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_room = db.query(models.Classroom).filter(models.Classroom.id == room_id).first()
    if not db_room:
        raise HTTPException(status_code=404, detail="Classroom not found")
    update_data = room.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_room, key, value)
    db.commit()
    db.refresh(db_room)
    return db_room

@router.delete("/classrooms/{room_id}")
def delete_classroom(room_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_room = db.query(models.Classroom).filter(models.Classroom.id == room_id).first()
    if not db_room:
        raise HTTPException(status_code=404, detail="Classroom not found")
    db.delete(db_room)
    db.commit()
    return {"ok": True}

# ---------- Schedules ----------
@router.get("/schedules", response_model=List[schemas.ScheduleOut])
def get_schedules(db: Session = Depends(get_db)):
    return db.query(models.Schedule).all()

@router.post("/schedules", response_model=schemas.ScheduleOut)
def create_schedule(sched: schemas.ScheduleCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_sched = models.Schedule(**sched.dict())
    db.add(db_sched)
    db.commit()
    db.refresh(db_sched)
    return db_sched

@router.put("/schedules/{sched_id}", response_model=schemas.ScheduleOut)
def update_schedule(sched_id: int, sched: schemas.ScheduleUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_sched = db.query(models.Schedule).filter(models.Schedule.id == sched_id).first()
    if not db_sched:
        raise HTTPException(status_code=404, detail="Schedule not found")
    update_data = sched.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_sched, key, value)
    db.commit()
    db.refresh(db_sched)
    return db_sched

@router.delete("/schedules/{sched_id}")
def delete_schedule(sched_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_sched = db.query(models.Schedule).filter(models.Schedule.id == sched_id).first()
    if not db_sched:
        raise HTTPException(status_code=404, detail="Schedule not found")
    db.delete(db_sched)
    db.commit()
    return {"ok": True}

# ---------- CourseSchedule (managed via course endpoints) ----------
@router.post("/courses/{course_id}/schedules", response_model=schemas.CourseOut)
def add_schedule_to_course(course_id: int, schedule_ids: List[int] = Body(...), db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    if current_user.role != "department_head" or course.department.head_user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    for sid in schedule_ids:
        sched = db.query(models.Schedule).filter(models.Schedule.id == sid).first()
        if sched:
            course.schedules.append(sched)
    db.commit()
    db.refresh(course)
    return course

# ---------- Enrollments ----------
@router.get("/enrollments", response_model=List[schemas.EnrollmentOut])
def get_enrollments(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    return db.query(models.Enrollment).all()

@router.post("/enrollments", response_model=schemas.EnrollmentOut)
def create_enrollment(enr: schemas.EnrollmentCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    # Only students
    if current_user.role != "student":
        raise HTTPException(status_code=403, detail="Only students can enroll")
    student_id = current_user.id
    # Duplicate
    existing = db.query(models.Enrollment).filter(
        models.Enrollment.student_id == student_id,
        models.Enrollment.course_id == enr.course_id,
        models.Enrollment.status == "enrolled"
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already enrolled")
    course = db.query(models.Course).filter(models.Course.id == enr.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    # Capacities
    current_count = db.query(models.Enrollment).filter(
        models.Enrollment.course_id == course.id,
        models.Enrollment.status == "enrolled"
    ).count()
    effective_capacity = course.classroom.capacity if course.classroom else course.capacity
    if current_count >= effective_capacity:
        raise HTTPException(status_code=400, detail="Course is full")
    # Prerequisites
    mandatory_prereqs = db.query(models.Prerequisite).filter(
        models.Prerequisite.course_id == course.id,
        models.Prerequisite.is_mandatory == True
    ).all()
    missing = []
    for prereq in mandatory_prereqs:
        completed = db.query(models.Enrollment).filter(
            models.Enrollment.student_id == student_id,
            models.Enrollment.course_id == prereq.prerequisite_course_id,
            models.Enrollment.status == "completed"
        ).first()
        if not completed:
            missing.append(prereq.prerequisite_course.title if prereq.prerequisite_course else str(prereq.prerequisite_course_id))
    if missing:
        raise HTTPException(status_code=400, detail="Missing mandatory prerequisites: " + ", ".join(missing))
    # Non-mandatory warning (return in response later; for simplicity we ignore warning in response)
    # Schedule conflict
    if check_schedule_conflict(db, student_id, course):
        raise HTTPException(status_code=400, detail="Schedule conflict with another enrolled course")
    # Credit limit
    if check_credit_limit(db, student_id, course):
        raise HTTPException(status_code=400, detail="Enrollment would exceed 30 credits limit per semester")
    # Create enrollment
    db_enr = models.Enrollment(student_id=student_id, course_id=course.id, enrolled_at=datetime.utcnow(), status="enrolled")
    db.add(db_enr)
    db.commit()
    db.refresh(db_enr)
    return db_enr

@router.put("/enrollments/{enr_id}/drop")
def drop_enrollment(enr_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    enr = db.query(models.Enrollment).filter(models.Enrollment.id == enr_id).first()
    if not enr:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    if enr.student_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    enr.status = "dropped"
    db.commit()
    return {"ok": True}

# ---------- Grades ----------
@router.get("/grades", response_model=List[schemas.GradeOut])
def get_grades(db: Session = Depends(get_db)):
    return db.query(models.Grade).all()

@router.post("/grades", response_model=schemas.GradeOut)
def create_grade(grade: schemas.GradeCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    # Check role: must be teacher of the course
    enrollment = db.query(models.Enrollment).filter(models.Enrollment.id == grade.enrollment_id).first()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    course = enrollment.course
    if current_user.role != "teacher" or course.teacher_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only the course instructor can assign grades")
    # One grade per enrollment
    existing = db.query(models.Grade).filter(models.Grade.enrollment_id == grade.enrollment_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Grade already exists for this enrollment")
    # Determine letter grade (simple scale)
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
    db_grade = models.Grade(
        enrollment_id=grade.enrollment_id,
        score=score,
        letter_grade=letter,
        graded_at=datetime.utcnow(),
        graded_by=current_user.id
    )
    db.add(db_grade)
    # Mark enrollment as completed
    enrollment.status = "completed"
    db.commit()
    db.refresh(db_grade)
    return db_grade

# ---------- Assignments ----------
@router.get("/assignments", response_model=List[schemas.AssignmentOut])
def get_assignments(db: Session = Depends(get_db)):
    return db.query(models.Assignment).all()

@router.post("/assignments", response_model=schemas.AssignmentOut)
def create_assignment(assgn: schemas.AssignmentCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    course = db.query(models.Course).filter(models.Course.id == assgn.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    if current_user.role != "teacher" or course.teacher_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only instructor can create assignments")
    db_assgn = models.Assignment(**assgn.dict())
    db.add(db_assgn)
    db.commit()
    db.refresh(db_assgn)
    return db_assgn

@router.put("/assignments/{assgn_id}", response_model=schemas.AssignmentOut)
def update_assignment(assgn_id: int, assgn: schemas.AssignmentUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_assgn = db.query(models.Assignment).filter(models.Assignment.id == assgn_id).first()
    if not db_assgn:
        raise HTTPException(status_code=404, detail="Assignment not found")
    course = db_assgn.course
    if current_user.role != "teacher" or course.teacher_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only instructor can update assignments")
    update_data = assgn.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_assgn, key, value)
    db.commit()
    db.refresh(db_assgn)
    return db_assgn

@router.delete("/assignments/{assgn_id}")
def delete_assignment(assgn_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_assgn = db.query(models.Assignment).filter(models.Assignment.id == assgn_id).first()
    if not db_assgn:
        raise HTTPException(status_code=404, detail="Assignment not found")
    course = db_assgn.course
    if current_user.role != "teacher" or course.teacher_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only instructor can delete assignments")
    db.delete(db_assgn)
    db.commit()
    return {"ok": True}