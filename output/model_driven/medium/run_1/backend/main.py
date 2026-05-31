from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from database import get_db
from models import Course, User, Enrollment, Grade, Assignment, Department
from schemas import CourseCreate, CourseResponse, CourseUpdate

router_users = APIRouter(prefix="/users", tags=["Users"])
router_departments = APIRouter(prefix="/departments", tags=["Departments"])
router_courses = APIRouter(prefix="/courses", tags=["Courses"])
router_enrollments = APIRouter(prefix="/enrollments", tags=["Enrollments"])
router_grades = APIRouter(prefix="/grades", tags=["Grades"])
router_assignments = APIRouter(prefix="/assignments", tags=["Assignments"])

# ... other endpoint definitions ...

# The original line had a missing closing parenthesis ')'.
# Fix: added the missing ')'.
@router_courses.put("/{item_id}", response_model=CourseResponse)
def update_course(item_id: int, course: CourseUpdate, db: Session = Depends(get_db)):
    db_course = db.query(Course).filter(Course.id == item_id).first()
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    for key, value in course.dict(exclude_unset=True).items():
        setattr(db_course, key, value)
    db.commit()
    db.refresh(db_course)
    return db_course

routers = [router_users, router_departments, router_courses, router_enrollments, router_grades, router_assignments]