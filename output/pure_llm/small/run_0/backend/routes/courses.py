from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from ..database import get_db
from ..models import Course, Enrollment
from ..schemas import CourseCreate, CourseUpdate, CourseOut

router = APIRouter()

def add_enrolled_count(course, db):
    count = db.query(func.count(Enrollment.id)).filter(Enrollment.course_id == course.id).scalar()
    course.enrolled_count = count
    return course

@router.get("/", response_model=List[CourseOut])
def list_courses(db: Session = Depends(get_db)):
    courses = db.query(Course).all()
    result = []
    for c in courses:
        c2 = add_enrolled_count(c, db)
        # Pydantic can handle extra attribute if we set it before serialization
        result.append(CourseOut.model_validate(c2))
    return result

@router.post("/", response_model=CourseOut, status_code=201)
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    db_course = Course(**course.model_dump())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    db_course = add_enrolled_count(db_course, db)
    return CourseOut.model_validate(db_course)

@router.get("/{course_id}", response_model=CourseOut)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    course = add_enrolled_count(course, db)
    return CourseOut.model_validate(course)

@router.put("/{course_id}", response_model=CourseOut)
def update_course(course_id: int, course_data: CourseUpdate, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    update_data = course_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(course, key, value)
    db.commit()
    db.refresh(course)
    course = add_enrolled_count(course, db)
    return CourseOut.model_validate(course)

@router.delete("/{course_id}", status_code=204)
def delete_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    db.delete(course)
    db.commit()
    return None