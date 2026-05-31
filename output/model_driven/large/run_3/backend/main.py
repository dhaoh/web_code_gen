"""
FastAPI routers for student_course_system_large.
Generated from model definition.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from .database import get_db

routers = []

# User routes
user_router = APIRouter(prefix="/users", tags=["users"])

@user_router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@user_router.get("/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.User).offset(skip).limit(limit).all()

@user_router.get("/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@user_router.put("/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in user.dict(exclude_unset=True).items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

@user_router.delete("/{user_id}", response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return db_user

routers.append(user_router)

# Department routes
dept_router = APIRouter(prefix="/departments", tags=["departments"])

@dept_router.post("/", response_model=schemas.Department)
def create_department(department: schemas.DepartmentCreate, db: Session = Depends(get_db)):
    db_dept = models.Department(**department.dict())
    db.add(db_dept)
    db.commit()
    db.refresh(db_dept)
    return db_dept

@dept_router.get("/", response_model=list[schemas.Department])
def read_departments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Department).offset(skip).limit(limit).all()

@dept_router.get("/{dept_id}", response_model=schemas.Department)
def read_department(dept_id: int, db: Session = Depends(get_db)):
    dept = db.query(models.Department).filter(models.Department.id == dept_id).first()
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")
    return dept

@dept_router.put("/{dept_id}", response_model=schemas.Department)
def update_department(dept_id: int, department: schemas.DepartmentUpdate, db: Session = Depends(get_db)):
    db_dept = db.query(models.Department).filter(models.Department.id == dept_id).first()
    if not db_dept:
        raise HTTPException(status_code=404, detail="Department not found")
    for key, value in department.dict(exclude_unset=True).items():
        setattr(db_dept, key, value)
    db.commit()
    db.refresh(db_dept)
    return db_dept

@dept_router.delete("/{dept_id}", response_model=schemas.Department)
def delete_department(dept_id: int, db: Session = Depends(get_db)):
    db_dept = db.query(models.Department).filter(models.Department.id == dept_id).first()
    if not db_dept:
        raise HTTPException(status_code=404, detail="Department not found")
    db.delete(db_dept)
    db.commit()
    return db_dept

routers.append(dept_router)

# Major routes
major_router = APIRouter(prefix="/majors", tags=["majors"])

@major_router.post("/", response_model=schemas.Major)
def create_major(major: schemas.MajorCreate, db: Session = Depends(get_db)):
    db_major = models.Major(**major.dict())
    db.add(db_major)
    db.commit()
    db.refresh(db_major)
    return db_major

@major_router.get("/", response_model=list[schemas.Major])
def read_majors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Major).offset(skip).limit(limit).all()

@major_router.get("/{major_id}", response_model=schemas.Major)
def read_major(major_id: int, db: Session = Depends(get_db)):
    major = db.query(models.Major).filter(models.Major.id == major_id).first()
    if not major:
        raise HTTPException(status_code=404, detail="Major not found")
    return major

@major_router.put("/{major_id}", response_model=schemas.Major)
def update_major(major_id: int, major: schemas.MajorUpdate, db: Session = Depends(get_db)):
    db_major = db.query(models.Major).filter(models.Major.id == major_id).first()
    if not db_major:
        raise HTTPException(status_code=404, detail="Major not found")
    for key, value in major.dict(exclude_unset=True).items():
        setattr(db_major, key, value)
    db.commit()
    db.refresh(db_major)
    return db_major

@major_router.delete("/{major_id}", response_model=schemas.Major)
def delete_major(major_id: int, db: Session = Depends(get_db)):
    db_major = db.query(models.Major).filter(models.Major.id == major_id).first()
    if not db_major:
        raise HTTPException(status_code=404, detail="Major not found")
    db.delete(db_major)
    db.commit()
    return db_major

routers.append(major_router)

# Course routes
course_router = APIRouter(prefix="/courses", tags=["courses"])

@course_router.post("/", response_model=schemas.Course)
def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    # Business logic checks
    if course.department_id:
        pass  # Placeholder for potential validation
    db_course = models.Course(**course.dict())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

@course_router.get("/", response_model=list[schemas.Course])
def read_courses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Course).offset(skip).limit(limit).all()

@course_router.get("/{course_id}", response_model=schemas.Course)
def read_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@course_router.put("/{course_id}", response_model=schemas.Course)
def update_course(course_id: int, course: schemas.CourseUpdate, db: Session = Depends(get_db)):
    db_course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    for key, value in course.dict(exclude_unset=True).items():
        setattr(db_course, key, value)
    db.commit()
    db.refresh(db_course)
    return db_course

@course_router.delete("/{course_id}", response_model=schemas.Course)
def delete_course(course_id: int, db: Session = Depends(get_db)):
    db_course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    db.delete(db_course)
    db.commit()
    return db_course

routers.append(course_router)

# Prerequisite routes
prereq_router = APIRouter(prefix="/prerequisites", tags=["prerequisites"])

@prereq_router.post("/", response_model=schemas.Prerequisite)
def create_prerequisite(prereq: schemas.PrerequisiteCreate, db: Session = Depends(get_db)):
    db_prereq = models.Prerequisite(**prereq.dict())
    db.add(db_prereq)
    db.commit()
    db.refresh(db_prereq)
    return db_prereq

@prereq_router.get("/", response_model=list[schemas.Prerequisite])
def read_prerequisites(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Prerequisite).offset(skip).limit(limit).all()

@prereq_router.get("/{prereq_id}", response_model=schemas.Prerequisite)
def read_prerequisite(prereq_id: int, db: Session = Depends(get_db)):
    prereq = db.query(models.Prerequisite).filter(models.Prerequisite.id == prereq_id).first()
    if not prereq:
        raise HTTPException(status_code=404, detail="Prerequisite not found")
    return prereq

@prereq_router.put("/{prereq_id}", response_model=schemas.Prerequisite)
def update_prerequisite(prereq_id: int, prereq: schemas.PrerequisiteUpdate, db: Session = Depends(get_db)):
    db_prereq = db.query(models.Prerequisite).filter(models.Prerequisite.id == prereq_id).first()
    if not db_prereq:
        raise HTTPException(status_code=404, detail="Prerequisite not found")
    for key, value in prereq.dict(exclude_unset=True).items():
        setattr(db_prereq, key, value)
    db.commit()
    db.refresh(db_prereq)
    return db_prereq

@prereq_router.delete("/{prereq_id}", response_model=schemas.Prerequisite)
def delete_prerequisite(prereq_id: int, db: Session = Depends(get_db)):
    db_prereq = db.query(models.Prerequisite).filter(models.Prerequisite.id == prereq_id).first()
    if not db_prereq:
        raise HTTPException(status_code=404, detail="Prerequisite not found")
    db.delete(db_prereq)
    db.commit()
    return db_prereq

routers.append(prereq_router)

# Classroom routes
classroom_router = APIRouter(prefix="/classrooms", tags=["classrooms"])

@classroom_router.post("/", response_model=schemas.Classroom)
def create_classroom(classroom: schemas.ClassroomCreate, db: Session = Depends(get_db)):
    db_classroom = models.Classroom(**classroom.dict())
    db.add(db_classroom)
    db.commit()
    db.refresh(db_classroom)
    return db_classroom

@classroom_router.get("/", response_model=list[schemas.Classroom])
def read_classrooms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Classroom).offset(skip).limit(limit).all()

@classroom_router.get("/{classroom_id}", response_model=schemas.Classroom)
def read_classroom(classroom_id: int, db: Session = Depends(get_db)):
    classroom = db.query(models.Classroom).filter(models.Classroom.id == classroom_id).first()
    if not classroom:
        raise HTTPException(status_code=404, detail="Classroom not found")
    return classroom

@classroom_router.put("/{classroom_id}", response_model=schemas.Classroom)
def update_classroom(classroom_id: int, classroom: schemas.ClassroomUpdate, db: Session = Depends(get_db)):
    db_classroom = db.query(models.Classroom).filter(models.Classroom.id == classroom_id).first()
    if not db_classroom:
        raise HTTPException(status_code=404, detail="Classroom not found")
    for key, value in classroom.dict(exclude_unset=True).items():
        setattr(db_classroom, key, value)
    db.commit()
    db.refresh(db_classroom)
    return db_classroom

@classroom_router.delete("/{classroom_id}", response_model=schemas.Classroom)
def delete_classroom(classroom_id: int, db: Session = Depends(get_db)):
    db_classroom = db.query(models.Classroom).filter(models.Classroom.id == classroom_id).first()
    if not db_classroom:
        raise HTTPException(status_code=404, detail="Classroom not found")
    db.delete(db_classroom)
    db.commit()
    return db_classroom

routers.append(classroom_router)

# Schedule routes
schedule_router = APIRouter(prefix="/schedules", tags=["schedules"])

@schedule_router.post("/", response_model=schemas.Schedule)
def create_schedule(schedule: schemas.ScheduleCreate, db: Session = Depends(get_db)):
    db_schedule = models.Schedule(**schedule.dict())
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule

@schedule_router.get("/", response_model=list[schemas.Schedule])
def read_schedules(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Schedule).offset(skip).limit(limit).all()

@schedule_router.get("/{schedule_id}", response_model=schemas.Schedule)
def read_schedule(schedule_id: int, db: Session = Depends(get_db)):
    schedule = db.query(models.Schedule).filter(models.Schedule.id == schedule_id).first()
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return schedule

@schedule_router.put("/{schedule_id}", response_model=schemas.Schedule)
def update_schedule(schedule_id: int, schedule: schemas.ScheduleUpdate, db: Session = Depends(get_db)):
    db_schedule = db.query(models.Schedule).filter(models.Schedule.id == schedule_id).first()
    if not db_schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    for key, value in schedule.dict(exclude_unset=True).items():
        setattr(db_schedule, key, value)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule

@schedule_router.delete("/{schedule_id}", response_model=schemas.Schedule)
def delete_schedule(schedule_id: int, db: Session = Depends(get_db)):
    db_schedule = db.query(models.Schedule).filter(models.Schedule.id == schedule_id).first()
    if not db_schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    db.delete(db_schedule)
    db.commit()
    return db_schedule

routers.append(schedule_router)

# CourseSchedule routes
course_schedule_router = APIRouter(prefix="/course-schedules", tags=["course-schedules"])

@course_schedule_router.post("/", response_model=schemas.CourseSchedule)
def create_course_schedule(cs: schemas.CourseScheduleCreate, db: Session = Depends(get_db)):
    db_cs = models.CourseSchedule(**cs.dict())
    db.add(db_cs)
    db.commit()
    db.refresh(db_cs)
    return db_cs

@course_schedule_router.get("/", response_model=list[schemas.CourseSchedule])
def read_course_schedules(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.CourseSchedule).offset(skip).limit(limit).all()

@course_schedule_router.get("/{cs_id}", response_model=schemas.CourseSchedule)
def read_course_schedule(cs_id: int, db: Session = Depends(get_db)):
    cs = db.query(models.CourseSchedule).filter(models.CourseSchedule.id == cs_id).first()
    if not cs:
        raise HTTPException(status_code=404, detail="CourseSchedule not found")
    return cs

@course_schedule_router.put("/{cs_id}", response_model=schemas.CourseSchedule)
def update_course_schedule(cs_id: int, cs: schemas.CourseScheduleUpdate, db: Session = Depends(get_db)):
    db_cs = db.query(models.CourseSchedule).filter(models.CourseSchedule.id == cs_id).first()
    if not db_cs:
        raise HTTPException(status_code=404, detail="CourseSchedule not found")