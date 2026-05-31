from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Table, UniqueConstraint
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

# Association table for many-to-many between Course and Schedule
course_schedule = Table(
    "course_schedule",
    Base.metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("course_id", Integer, ForeignKey("courses.id"), nullable=False),
    Column("schedule_id", Integer, ForeignKey("schedules.id"), nullable=False),
)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)  # student, teacher, department_head, admin
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    major_id = Column(Integer, ForeignKey("majors.id"), nullable=True)

    major = relationship("Major", back_populates="users")
    # Courses taught by this user (teacher)
    courses_taught = relationship("Course", back_populates="teacher", foreign_keys="Course.teacher_id")

class Department(Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    code = Column(String, unique=True, nullable=False)
    head_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    head = relationship("User")
    courses = relationship("Course", back_populates="department")
    majors = relationship("Major", back_populates="department")

class Major(Base):
    __tablename__ = "majors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    code = Column(String, unique=True, nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    total_credits_required = Column(Integer, nullable=False)

    department = relationship("Department", back_populates="majors")
    users = relationship("User", back_populates="major")

class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    code = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    capacity = Column(Integer, nullable=False)
    credits = Column(Integer, nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    classroom_id = Column(Integer, ForeignKey("classrooms.id"), nullable=True)
    semester = Column(String, nullable=False)

    department = relationship("Department", back_populates="courses")
    teacher = relationship("User", back_populates="courses_taught", foreign_keys=[teacher_id])
    classroom = relationship("Classroom", back_populates="courses")
    schedules = relationship("Schedule", secondary=course_schedule, back_populates="courses")
    enrollments = relationship("Enrollment", back_populates="course")
    assignments = relationship("Assignment", back_populates="course")
    prerequisites = relationship("Prerequisite", back_populates="course", foreign_keys="Prerequisite.course_id")
    required_for = relationship("Prerequisite", back_populates="prerequisite_course", foreign_keys="Prerequisite.prerequisite_course_id")

class Prerequisite(Base):
    __tablename__ = "prerequisites"
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    prerequisite_course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    is_mandatory = Column(Boolean, nullable=False)

    course = relationship("Course", back_populates="prerequisites", foreign_keys=[course_id])
    prerequisite_course = relationship("Course", back_populates="required_for", foreign_keys=[prerequisite_course_id])

class Classroom(Base):
    __tablename__ = "classrooms"
    id = Column(Integer, primary_key=True, index=True)
    building = Column(String, nullable=False)
    room_number = Column(String, nullable=False)
    capacity = Column(Integer, nullable=False)

    courses = relationship("Course", back_populates="classroom")

class Schedule(Base):
    __tablename__ = "schedules"
    id = Column(Integer, primary_key=True, index=True)
    day_of_week = Column(Integer, nullable=False)  # 0=Monday, ..., 6=Sunday
    start_time = Column(String, nullable=False)  # HH:MM
    end_time = Column(String, nullable=False)    # HH:MM

    courses = relationship("Course", secondary=course_schedule, back_populates="schedules")

class Enrollment(Base):
    __tablename__ = "enrollments"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    enrolled_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, nullable=False, default="enrolled")  # enrolled, dropped, completed

    student = relationship("User")
    course = relationship("Course", back_populates="enrollments")
    grade = relationship("Grade", back_populates="enrollment", uselist=False)

class Grade(Base):
    __tablename__ = "grades"
    id = Column(Integer, primary_key=True, index=True)
    enrollment_id = Column(Integer, ForeignKey("enrollments.id"), unique=True, nullable=False)
    score = Column(Float, nullable=False)
    letter_grade = Column(String, nullable=True)
    graded_at = Column(DateTime, default=datetime.utcnow)
    graded_by = Column(Integer, ForeignKey("users.id"), nullable=True)

    enrollment = relationship("Enrollment", back_populates="grade")
    grader = relationship("User")

class Assignment(Base):
    __tablename__ = "assignments"
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    due_date = Column(DateTime, nullable=False)
    max_score = Column(Integer, nullable=False)

    course = relationship("Course", back_populates="assignments")