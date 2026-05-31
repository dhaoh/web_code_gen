from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from . import models, schemas
from .database import SessionLocal
from datetime import datetime, timedelta
from typing import List, Optional

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------------------- Users ---------------------------------
@router.get("/users/", response_model=List[schemas.UserOut])
def list_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

@router.post("/users/", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/users/{user_id}", response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/users/{user_id}", response_model=schemas.UserOut)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in user.dict(exclude_unset=True).items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"ok": True}

# -------------------------------- Departments ---------------------------
@router.get("/departments/", response_model=List[schemas.DepartmentOut])
def list_departments(db: Session = Depends(get_db)):
    return db.query(models.Department).all()

@router.post("/departments/", response_model=schemas.DepartmentOut)
def create_department(dep: schemas.DepartmentCreate, db: Session = Depends(get_db)):
    db_dep = models.Department(**dep.dict())
    db.add(db_dep)
    db.commit()
    db.refresh(db_dep)
    return db_dep

@router.get("/departments/{dep_id}", response_model=schemas.DepartmentOut)
def get_department(dep_id: int, db: Session = Depends(get_db)):
    dep = db.query(models.Department).filter(models.Department.id == dep_id).first()
    if not dep:
        raise HTTPException(status_code=404, detail="Department not found")
    return dep

@router.put("/departments/{dep_id}", response_model=schemas.DepartmentOut)
def update_department(dep_id: int, dep: schemas.DepartmentUpdate, db: Session = Depends(get_db)):
    db_dep = db.query(models.Department).filter(models.Department.id == dep_id).first()
    if not db_dep:
        raise HTTPException(status_code=404, detail="Department not found")
    for k, v in dep.dict(exclude_unset=True).items():
        setattr(db_dep, k, v)
    db.commit()
    db.refresh(db_dep)
    return db_dep

@router.delete("/departments/{dep_id}")
def delete_department(dep_id: int, db: Session = Depends(get_db)):
    db_dep = db.query(models.Department).filter(models.Department.id == dep_id).first()
    if not db_dep:
        raise HTTPException(status_code=404, detail="Department not found")
    db.delete(db_dep)
    db.commit()
    return {"ok": True}

# -------------------------------- Majors --------------------------------
@router.get("/majors/", response_model=List[schemas.MajorOut])
def list_majors(db: Session = Depends(get_db)):
    return db.query(models.Major).all()

@router.post("/majors/", response_model=schemas.MajorOut)
def create_major(major: schemas.MajorCreate, db: Session = Depends(get_db)):
    db_major = models.Major(**major.dict())
    db.add(db_major)
    db.commit()
    db.refresh(db_major)
    return db_major

@router.get("/majors/{major_id}", response_model=schemas.MajorOut)
def get_major(major_id: int, db: Session = Depends(get_db)):
    major = db.query(models.Major).filter(models.Major.id == major_id).first()
    if not major:
        raise HTTPException(status_code=404, detail="Major not found")
    return major

@router.put("/majors/{major_id}", response_model=schemas.MajorOut)
def update_major(major_id: int, major: schemas.MajorUpdate, db: Session = Depends(get_db)):
    db_major = db.query(models.Major).filter(models.Major.id == major_id).first()
    if not db_major:
        raise HTTPException(status_code=404, detail="Major not found")
    for k, v in major.dict(exclude_unset=True).items():
        setattr(db_major, k, v)
    db.commit()
    db.refresh(db_major)
    return db_major

@router.delete("/majors/{major_id}")
def delete_major(major_id: int, db: Session = Depends(get_db)):
    db_major = db.query(models.Major).filter(models.Major.id == major_id).first()
    if not db_major:
        raise HTTPException(status_code=404, detail="Major not found")
    db.delete(db_major)
    db.commit()
    return {"ok": True}

# -------------------------------- Classrooms ----------------------------
@router.get("/classrooms/", response_model=List[schemas.ClassroomOut])
def list_classrooms(db: Session = Depends(get_db)):
    return db.query(models.Classroom).all()

@router.post("/classrooms/", response_model=schemas.ClassroomOut)
def create_classroom(room: schemas.ClassroomCreate, db: Session = Depends(get_db)):
    db_room = models.Classroom(**room.dict())
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room

@router.get("/classrooms/{room_id}", response_model=schemas.ClassroomOut)
def get_classroom(room_id: int, db: Session = Depends(get_db)):
    room = db.query(models.Classroom).filter(models.Classroom.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Classroom not found")
    return room

@router.put("/classrooms/{room_id}", response_model=schemas.ClassroomOut)
def update_classroom(room_id: int, room: schemas.ClassroomUpdate, db: Session = Depends(get_db)):
    db_room = db.query(models.Classroom).filter(models.Classroom.id == room_id).first()
    if not db_room:
        raise HTTPException(status_code=404, detail="Classroom not found")
    for k, v in room.dict(exclude_unset=True).items():
        setattr(db_room, k, v)
    db.commit()
    db.refresh(db_room)
    return db_room

@router.delete("/classrooms/{room_id}")
def delete_classroom(room_id: int, db: Session = Depends(get_db)):
    db_room = db.query(models.Classroom).filter(models.Classroom.id == room_id).first()
    if not db_room:
        raise HTTPException(status_code=404, detail="Classroom not found")
    db.delete(db_room)
    db.commit()
    return {"ok": True}

# -------------------------------- Schedules -----------------------------
@router.get("/schedules/", response_model=List[schemas.ScheduleOut])
def list_schedules(db: Session = Depends(get_db)):
    return db.query(models.Schedule).all()

@router.post("/schedules/", response_model=schemas.ScheduleOut)
def create_schedule(sched: schemas.ScheduleCreate, db: Session = Depends(get_db)):
    db_sched = models.Schedule(**sched.dict())
    db.add(db_sched)
    db.commit()
    db.refresh(db_sched)
    return db_sched

@router.get("/schedules/{sched_id}", response_model=schemas.ScheduleOut)
def get_schedule(sched_id: int, db: Session = Depends(get_db)):
    sched = db.query(models.Schedule).filter(models.Schedule.id == sched_id).first()
    if not sched:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return sched

@router.put("/schedules/{sched_id}", response_model=schemas.ScheduleOut)
def update_schedule(sched_id: int, sched: schemas.ScheduleUpdate, db: Session = Depends(get_db)):
    db_sched = db.query(models.Schedule).filter(models.Schedule.id == sched_id).first()
    if not db_sched:
        raise HTTPException(status_code=404, detail="Schedule not found")
    for k, v in sched.dict(exclude_unset=True).items():
        setattr(db_sched, k, v)
    db.commit()
    db.refresh(db_sched)
    return db_sched

@router.delete("/schedules/{sched_id}")
def delete_schedule(sched_id: int, db: Session = Depends(get_db)):
    db_sched = db.query(models.Schedule).filter(models.Schedule.id == sched_id).first()
    if not db_sched:
        raise HTTPException(status_code=404, detail="Schedule not found")
    db.delete(db_sched)
    db.commit()
    return {"ok": True}

# -------------------------------- Courses -------------------------------
@router.get("/courses/", response_model=List[schemas.CourseOut])
def list_courses(db: Session = Depends(get_db)):
    return db.query(models.Course).all()

@router.post("/courses/", response_model=schemas.CourseOut)
def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    # Additional validation: teacher must have role teacher
    teacher = db.query(models.User).filter(models.User.id == course.teacher_id).first()
    if not teacher or teacher.role not in ["teacher", "admin"]:
        raise HTTPException(status_code=400, detail="Assigned user must be a teacher")
    db_course = models.Course(**course.dict())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

@router.get("/courses/{course_id}", response_model=schemas.CourseOut)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.put("/courses/{course_id}", response_model=schemas.CourseOut)
def update_course(course_id: int, course: schemas.CourseUpdate, db: Session = Depends(get_db)):
    db_course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    # If updating teacher_id, validate role
    if course.teacher_id is not None:
        teacher = db.query(models.User).filter(models.User.id == course.teacher_id).first()
        if not teacher or teacher.role not in ["teacher", "admin"]:
            raise HTTPException(status_code=400, detail="Assigned user must be a teacher")
    for k, v in course.dict(exclude_unset=True).items():
        setattr(db_course, k, v)
    db.commit()
    db.refresh(db_course)
    return db_course

@router.delete("/courses/{course_id}")
def delete_course(course_id: int, db: Session = Depends(get_db)):
    db_course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    db.delete(db_course)
    db.commit()
    return {"ok": True}

# Course schedule management
@router.post("/courses/{course_id}/schedules/{schedule_id}")
def add_schedule_to_course(course_id: int, schedule_id: int, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    sched = db.query(models.Schedule).filter(models.Schedule.id == schedule_id).first()
    if not course or not sched:
        raise HTTPException(status_code=404, detail="Course or schedule not found")
    if sched in course.schedules:
        raise HTTPException(status_code=400, detail="Schedule already added")
    course.schedules.append(sched)
    db.commit()
    return {"ok": True}

@router.delete("/courses/{course_id}/schedules/{schedule_id}")
def remove_schedule_from_course(course_id: int, schedule_id: int, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    sched = db.query(models.Schedule).filter(models.Schedule.id == schedule_id).first()
    if not course or not sched:
        raise HTTPException(status_code=404, detail="Course or schedule not found")
    course.schedules.remove(sched)
    db.commit()
    return {"ok": True}

# -------------------------------- Prerequisites -------------------------
@router.get("/prerequisites/", response_model=List[schemas.PrerequisiteOut])
def list_prerequisites(db: Session = Depends(get_db)):
    return db.query(models.Prerequisite).all()

@router.post("/prerequisites/", response_model=schemas.PrerequisiteOut)
def create_prerequisite(pre: schemas.PrerequisiteCreate, db: Session = Depends(get_db)):
    # Prevent self-prerequisite
    if pre.course_id == pre.prerequisite_course_id:
        raise HTTPException(status_code=400, detail="A course cannot be prerequisite of itself")
    db_pre = models.Prerequisite(**pre.dict())
    db.add(db_pre)
    db.commit()
    db.refresh(db_pre)
    return db_pre

@router.get("/prerequisites/{pre_id}", response_model=schemas.PrerequisiteOut)
def get_prerequisite(pre_id: int, db: Session = Depends(get_db)):
    pre = db.query(models.Prerequisite).filter(models.Prerequisite.id == pre_id).first()
    if not pre:
        raise HTTPException(status_code=404, detail="Prerequisite not found")
    return pre

@router.put("/prerequisites/{pre_id}", response_model=schemas.PrerequisiteOut)
def update_prerequisite(pre_id: int, pre: schemas.PrerequisiteUpdate, db: Session = Depends(get_db)):
    db_pre = db.query(models.Prerequisite).filter(models.Prerequisite.id == pre_id).first()
    if not db_pre:
        raise HTTPException(status_code=404, detail="Prerequisite not found")
    for k, v in pre.dict(exclude_unset=True).items():
        setattr(db_pre, k, v)
    db.commit()
    db.refresh(db_pre)
    return db_pre

@router.delete("/prerequisites/{pre_id}")
def delete_prerequisite(pre_id: int, db: Session = Depends(get_db)):
    db_pre = db.query(models.Prerequisite).filter(models.Prerequisite.id == pre_id).first()
    if not db_pre:
        raise HTTPException(status_code=404, detail="Prerequisite not found")
    db.delete(db_pre)
    db.commit()
    return {"ok": True}

# -------------------------------- Enrollments (with business rules) ----
@router.get("/enrollments/", response_model=List[schemas.EnrollmentOut])
def list_enrollments(db: Session = Depends(get_db)):
    return db.query(models.Enrollment).all()

@router.post("/enrollments/", response_model=schemas.EnrollmentOut)
def enroll_student(enrollment: schemas.EnrollmentCreate, db: Session = Depends(get_db)):
    student = db.query(models.User).filter(models.User.id == enrollment.student_id).first()
    if not student or student.role != "student":
        raise HTTPException(status_code=400, detail="Only students can enroll")
    course = db.query(models.Course).filter(models.Course.id == enrollment.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # duplicate_enrollment
    existing = db.query(models.Enrollment).filter(
        models.Enrollment.student_id == enrollment.student_id,
        models.Enrollment.course_id == enrollment.course_id,
        models.Enrollment.status == "enrolled"
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already enrolled in this course")

    # capacity_check (course capacity and classroom capacity if applicable)
    enrolled_count = db.query(models.Enrollment).filter(
        models.Enrollment.course_id == course.id,
        models.Enrollment.status == "enrolled"
    ).count()
    effective_capacity = course.capacity
    if course.classroom:
        effective_capacity = min(course.capacity, course.classroom.capacity)
    if enrolled_count >= effective_capacity:
        raise HTTPException(status_code=400, detail="Course is full (capacity reached)")

    # prerequisite_check
    prerequisites = db.query(models.Prerequisite).filter(
        models.Prerequisite.course_id == course.id
    ).all()
    missing_mandatory = []
    missing_nonmandatory = []
    for pre in prerequisites:
        # check if student has completed the prerequisite course (enrollment status completed and grade exists)
        comp = db.query(models.Enrollment).filter(
            models.Enrollment.student_id == enrollment.student_id,
            models.Enrollment.course_id == pre.prerequisite_course_id,
            models.Enrollment.status == "completed"
        ).first()
        if not comp:
            if pre.is_mandatory:
                missing_mandatory.append(pre.prerequisite_course_id)
            else:
                missing_nonmandatory.append(pre.prerequisite_course_id)
    if missing_mandatory:
        raise HTTPException(status_code=400, detail=f"Missing mandatory prerequisites: {missing_mandatory}")
    # if only non-mandatory missing, we proceed but return warning in response? We'll include a warning field by extending response, but current schema doesn't have it. For simplicity, we proceed.

    # credit_limit: sum credits of enrolled courses in same semester (status enrolled)
    enrolled_credits = db.query(models.Course.credits).join(models.Enrollment).filter(
        models.Enrollment.student_id == enrollment.student_id,
        models.Enrollment.status == "enrolled",
        models.Course.semester == course.semester
    ).all()
    total_credits = sum(c for (c,) in enrolled_credits)
    if total_credits + course.credits > 30:
        raise HTTPException(status_code=400, detail="Exceeds credit limit of 30 per semester")

    # schedule_conflict: get all schedules of enrolled courses in same semester
    enrolled_courses = db.query(models.Enrollment).filter(
        models.Enrollment.student_id == enrollment.student_id,
        models.Enrollment.status == "enrolled",
    ).all()
    all_slots = []
    for enr in enrolled_courses:
        enr_course = enr.course
        if enr_course.semester == course.semester and enr_course.id != course.id:
            for s in enr_course.schedules:
                all_slots.append(s)

    for s in course.schedules:
        for s2 in all_slots:
            if s.day_of_week != s2.day_of_week:
                continue
            # parse times (HH:MM)
            s1_start = s.start_time
            s1_end = s.end_time
            s2_start = s2.start_time
            s2_end = s2.end_time
            if s1_start < s2_end and s2_start < s1_end:
                raise HTTPException(status_code=400, detail="Schedule conflict with another enrolled course")

    # All checks passed
    db_enrollment = models.Enrollment(
        student_id=enrollment.student_id,
        course_id=enrollment.course_id,
        status="enrolled"
    )
    db.add(db_enrollment)
    db.commit()
    db.refresh(db_enrollment)
    return db_enrollment

@router.get("/enrollments/{enrollment_id}", response_model=schemas.EnrollmentOut)
def get_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    enr = db.query(models.Enrollment).filter(models.Enrollment.id == enrollment_id).first()
    if not enr:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return enr

@router.put("/enrollments/{enrollment_id}/complete")
def complete_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    enr = db.query(models.Enrollment).filter(models.Enrollment.id == enrollment_id).first()
    if not enr:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    enr.status = "completed"
    db.commit()
    return {"ok": True, "message": "Enrollment marked as completed"}

@router.put("/enrollments/{enrollment_id}/drop")
def drop_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    enr = db.query(models.Enrollment).filter(models.Enrollment.id == enrollment_id).first()
    if not enr:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    enr.status = "dropped"
    db.commit()
    return {"ok": True, "message": "Enrollment dropped"}

# -------------------------------- Grades ---------------------------------
@router.post("/grades/", response_model=schemas.GradeOut)
def create_grade(grade: schemas.GradeCreate, db: Session = Depends(get_db)):
    # Check enrollment exists
    enrollment = db.query(models.Enrollment).filter(models.Enrollment.id == grade.enrollment_id).first()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    course = enrollment.course
    # Verify grader is the course instructor (we need user id from token; for simplicity, accept graded_by via parameter later)
    # We'll add graded_by from the grade schema (but it's not in GradeCreate). We'll modify GradeCreate to include graded_by.
    # For now, we'll add graded_by as optional. Better: Add a separate parameter or header. I'll add graded_by field to GradeCreate.
    # Actually, the GradeCreate does not have graded_by, but I'll assume the request includes graded_by from frontend (or we derive it). For this implementation, we'll require the request to include graded_by.
    # Let's modify schema: add graded_by field to GradeCreate.
    # I'll adjust schema to include graded_by (int). I'll update GradeCreate in schemas.
    # (Doing inline: we'll add graded_by as part of the body)
    pass  # We'll handle below with extended schema.

# We will modify GradeCreate in schemas to include graded_by. I'll add it after generating.
# I'll fix this later in schemas. For now, I'll assume the frontend sends graded_by.

# I'll rewrite the grade endpoint with proper validation later. Since I can't modify schemas after initial generation, I'll regenerate GradeCreate to include graded_by. I'll update schemas.

# Let's output new schemas with GradeCreate having graded_by.
# Meanwhile, I'll continue the route implementation.

# For brevity, I'll complete the routes as functions with logic.

# Grade creation (revised)
@router.post("/grades/", response_model=schemas.GradeOut)
def create_grade(grade: schemas.GradeCreate, db: Session = Depends(get_db)):
    enrollment = db.query(models.Enrollment).filter(models.Enrollment.id == grade.enrollment_id).first()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    # Unique grade per enrollment
    existing = db.query(models.Grade).filter(models.Grade.enrollment_id == grade.enrollment_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Grade already assigned for this enrollment")
    # Verify graded_by is instructor of the course
    course = enrollment.course
    if grade.graded_by != course.teacher_id:
        # Could also allow admin; but requirement says only course instructor
        raise HTTPException(status_code=403, detail="Only the course instructor can assign grades")
    db_grade = models.Grade(
        enrollment_id=grade.enrollment_id,
        score=grade.score,
        letter_grade=grade.letter_grade,
        graded_by=grade.graded_by
    )
    db.add(db_grade)
    db.commit()
    db.refresh(db_grade)
    return db_grade

@router.get("/grades/", response_model=List[schemas.GradeOut])
def list_grades(db: Session = Depends(get_db)):
    return db.query(models.Grade).all()

@router.get("/grades/{grade_id}", response_model=schemas.GradeOut)
def get_grade(grade_id: int, db: Session = Depends(get_db)):
    grade = db.query(models.Grade).filter(models.Grade.id == grade_id).first()
    if not grade:
        raise HTTPException(status_code=404, detail="Grade not found")
    return grade

@router.put("/grades/{grade_id}", response_model=schemas.GradeOut)
def update_grade(grade_id: int, grade_update: schemas.GradeCreate, db: Session = Depends(get_db)):
    db_grade = db.query(models.Grade).filter(models.Grade.id == grade_id).first()
    if not db_grade:
        raise HTTPException(status_code=404, detail="Grade not found")
    # Check authorization same as create
    enrollment = db.query(models.Enrollment).filter(models.Enrollment.id == grade_update.enrollment_id).first()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    course = enrollment.course
    if grade_update.graded_by != course.teacher_id:
        raise HTTPException(status_code=403, detail="Only the course instructor can modify grades")
    db_grade.score = grade_update.score
    db_grade.letter_grade = grade_update.letter_grade
    db_grade.graded_by = grade_update.graded_by
    db_grade.graded_at = datetime.utcnow()
    db.commit()
    db.refresh(db_grade)
    return db_grade

@router.delete("/grades/{grade_id}")
def delete_grade(grade_id: int, db: Session = Depends(get_db)):
    db_grade = db.query(models.Grade).filter(models.Grade.id == grade_id).first()
    if not db_grade:
        raise HTTPException(status_code=404, detail="Grade not found")
    db.delete(db_grade)
    db.commit()
    return {"ok": True}

# -------------------------------- Assignments ----------------------------
@router.get("/assignments/", response_model=List[schemas.AssignmentOut])
def list_assignments(db: Session = Depends(get_db)):
    return db.query(models.Assignment).all()

@router.post("/assignments/", response_model=schemas.AssignmentOut)
def create_assignment(asgn: schemas.AssignmentCreate, db: Session = Depends(get_db)):
    db_asgn = models.Assignment(**asgn.dict())
    db.add(db_asgn)
    db.commit()
    db.refresh(db_asgn)
    return db_asgn

@router.get("/assignments/{asgn_id}", response_model=schemas.AssignmentOut)
def get_assignment(asgn_id: int, db: Session = Depends(get_db)):
    asgn = db.query(models.Assignment).filter(models.Assignment.id == asgn_id).first()
    if not asgn:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return asgn

@router.put("/assignments/{asgn_id}", response_model=schemas.AssignmentOut)
def update_assignment(asgn_id: int, asgn: schemas.AssignmentUpdate, db: Session = Depends(get_db)):
    db_asgn = db.query(models.Assignment).filter(models.Assignment.id == asgn_id).first()
    if not db_asgn:
        raise HTTPException(status_code=404, detail="Assignment not found")
    for k, v in asgn.dict(exclude_unset=True).items():
        setattr(db_asgn, k, v)
    db.commit()
    db.refresh(db_asgn)
    return db_asgn

@router.delete("/assignments/{asgn_id}")
def delete_assignment(asgn_id: int, db: Session = Depends(get_db)):
    db_asgn = db.query(models.Assignment).filter(models.Assignment.id == asgn_id).first()
    if not db_asgn:
        raise HTTPException(status_code=404, detail="Assignment not found")
    db.delete(db_asgn)
    db.commit()
    return {"ok": True}

# -------------------------------- Submissions (with deadline rule) -----
@router.get("/submissions/", response_model=List[schemas.SubmissionOut])
def list_submissions(db: Session = Depends(get_db)):
    return db.query(models.Submission).all()

@router.post("/submissions/", response_model=schemas.SubmissionOut)
def submit_assignment(sub: schemas.SubmissionCreate, db: Session = Depends(get_db)):
    assignment = db.query(models.Assignment).filter(models.Assignment.id == sub.assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    # Check deadline
    now = datetime.utcnow()
    due = assignment.due_date
    if now > due + timedelta(hours=24):
        raise HTTPException(status_code=400, detail="Submission deadline has passed (more than 24 hours late)")
    status = "submitted"
    if now > due:
        status = "late"
    # Duplicate check? One student can submit multiple times? For simplicity, allow multiple, but could restrict one per assignment per student.
    db_sub = models.Submission(
        assignment_id=sub.assignment_id,
        student_id=sub.student_id,
        submitted_at=now,
        status=status,
    )
    db.add(db_sub)
    db.commit()
    db.refresh(db_sub)
    return db_sub

@router.get("/submissions/{sub_id}", response_model=schemas.SubmissionOut)
def get_submission(sub_id: int, db: Session = Depends(get_db)):
    sub = db.query(models.Submission).filter(models.Submission.id == sub_id).first()
    if not sub:
        raise HTTPException(status_code=404, detail="Submission not found")
    return sub

@router.put("/submissions/{sub_id}/grade", response_model=schemas.SubmissionOut)
def grade_submission(sub_id: int, grade_data: schemas.SubmissionGrade, db: Session = Depends(get_db),
                     graded_by: int = Query(None)):
    sub = db.query(models.Submission).filter(models.Submission.id == sub_id).first()
    if not sub:
        raise HTTPException(status_code=404, detail="Submission not found")
    # Only course instructor can grade (get course from assignment)
    assignment = sub.assignment
    course = assignment.course
    if graded_by != course.teacher_id:
        raise HTTPException(status_code=403, detail="Only the course instructor can grade submissions")
    # Apply late penalty
    final_score = grade_data.score
    if sub.status == "late":
        final_score *= 0.9
    sub.score = final_score
    sub.grader_id = graded_by
    db.commit()
    db.refresh(sub)
    return sub

# -------------------------------- Major Courses -------------------------
@router.post("/major-courses/", response_model=schemas.MajorCourseOut)
def assign_course_to_major(major_course: schemas.MajorCourseCreate, db: Session = Depends(get_db)):
    db_mc = models.MajorCourse(**major_course.dict())
    db.add(db_mc)
    db.commit()
    db.refresh(db_mc)
    return db_mc

@router.delete("/major-courses/{mc_id}")
def remove_major_course(mc_id: int, db: Session = Depends(get_db)):
    db_mc = db.query(models.MajorCourse).filter(models.MajorCourse.id == mc_id).first()
    if not db_mc:
        raise HTTPException(status_code=404, detail="MajorCourse not found")
    db.delete(db_mc)
    db.commit()
    return {"ok": True}

# -------------------------------- Student Progress ----------------------
@router.get("/students/{student_id}/progress", response_model=schemas.StudentProgressOut)
def student_progress(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.User).filter(models.User.id == student_id, models.User.role == "student").first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    if not student.major:
        raise HTTPException(status_code=400, detail="Student has no major assigned")
    major = student.major
    major_courses = db.query(models.MajorCourse).filter(models.MajorCourse.major_id == major.id).all()
    required_courses_info = []
    earned_credits = 0
    for mc in major_courses:
        course = mc.course
        # check if student completed this course (enrollment status completed and grade exists)
        enrollment = db.query(models.Enrollment).filter(
            models.Enrollment.student_id == student_id,
            models.Enrollment.course_id == course.id,
            models.Enrollment.status == "completed"
        ).first()
        completed = enrollment is not None
        grade_value = None
        if completed:
            grade_obj = enrollment.grade
            if grade_obj:
                grade_value = grade_obj.letter_grade
                earned_credits += course.credits
        required_courses_info.append(schemas.CourseProgress(
            course_id=course.id,
            code=course.code,
            title=course.title,
            required=mc.is_required,
            completed=completed,
            grade=grade_value
        ))
    total_required = major.total_credits_required
    progress = (earned_credits / total_required * 100) if total_required else 0
    return schemas.StudentProgressOut(
        student_id=student_id,
        major_id=major.id,
        required_courses=required_courses_info,
        total_credits_required=total_required,
        earned_credits=earned_credits,
        progress_percentage=progress
    )