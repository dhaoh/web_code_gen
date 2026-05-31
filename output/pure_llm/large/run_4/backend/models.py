from sqlalchemy import (
    Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Table, Text
)
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

# Many-to-many: Course <-> Schedule
course_schedule_table = Table(
    "course_schedule",
    Base.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("course_id", Integer, ForeignKey("courses.id", ondelete="CASCADE")),
    Column("schedule_id", Integer, ForeignKey("schedules.id", ondelete="CASCADE")),
)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)  # student, teacher, department_head, admin
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    major_id = Column(Integer, ForeignKey("majors.id"))

    major = relationship("Major", back_populates="users")
    taught_courses = relationship("Course", back_populates="teacher", foreign_keys="Course.teacher_id")
    head_of_department = relationship("Department", back_populates="head_user", foreign_keys="Department.head_user_id")
    enrollments = relationship("Enrollment", back_populates="student", foreign_keys="Enrollment.student_id")
    submissions = relationship("Submission", back_populates="student")

class Department(Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    code = Column(String, unique=True, nullable=False)
    head_user_id = Column(Integer, ForeignKey("users.id"))

    head_user = relationship("User", back_populates="head_of_department", foreign_keys=[head_user_id])
    courses = relationship("Course", back_populates="department")
    majors = relationship("Major", back_populates="department")

class Major(Base):
    __tablename__ = "majors"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    code = Column(String, unique=True, nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    total_credits_required = Column(Integer, nullable=False)

    department = relationship("Department", back_populates="majors")
    users = relationship("User", back_populates="major")
    major_courses = relationship("MajorCourse", back_populates="major")

class MajorCourse(Base):
    __tablename__ = "major_courses"
    id = Column(Integer, primary_key=True, autoincrement=True)
    major_id = Column(Integer, ForeignKey("majors.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    is_required = Column(Boolean, nullable=False, default=True)

    major = relationship("Major", back_populates="major_courses")
    course = relationship("Course", back_populates="major_courses")

class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    code = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable=True)
    capacity = Column(Integer, nullable=False)
    credits = Column(Integer, nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    classroom_id = Column(Integer, ForeignKey("classrooms.id"), nullable=True)
    semester = Column(String, nullable=False)

    department = relationship("Department", back_populates="courses")
    teacher = relationship("User", back_populates="taught_courses", foreign_keys=[teacher_id])
    classroom = relationship("Classroom", back_populates="courses")
    schedules = relationship("Schedule", secondary=course_schedule_table, back_populates="courses")
    prerequisites = relationship("Prerequisite", back_populates="course", foreign_keys="Prerequisite.course_id")
    prerequisite_for = relationship("Prerequisite", back_populates="prerequisite_course", foreign_keys="Prerequisite.prerequisite_course_id")
    enrollments = relationship("Enrollment", back_populates="course")
    assignments = relationship("Assignment", back_populates="course")
    major_courses = relationship("MajorCourse", back_populates="course")

class Prerequisite(Base):
    __tablename__ = "prerequisites"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    prerequisite_course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    is_mandatory = Column(Boolean, nullable=False)

    course = relationship("Course", back_populates="prerequisites", foreign_keys=[course_id])
    prerequisite_course = relationship("Course", back_populates="prerequisite_for", foreign_keys=[prerequisite_course_id])

class Classroom(Base):
    __tablename__ = "classrooms"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    building = Column(String, nullable=False)
    room_number = Column(String, nullable=False)
    capacity = Column(Integer, nullable=False)

    courses = relationship("Course", back_populates="classroom")

class Schedule(Base):
    __tablename__ = "schedules"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    day_of_week = Column(Integer, nullable=False)  # 0=Monday...6=Sunday
    start_time = Column(String, nullable=False)   # HH:MM format
    end_time = Column(String, nullable=False)

    courses = relationship("Course", secondary=course_schedule_table, back_populates="schedules")

class Enrollment(Base):
    __tablename__ = "enrollments"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    enrolled_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    status = Column(String, nullable=False, default="enrolled")

    student = relationship("User", back_populates="enrollments", foreign_keys=[student_id])
    course = relationship("Course", back_populates="enrollments")
    grade = relationship("Grade", back_populates="enrollment", uselist=False)

class Grade(Base):
    __tablename__ = "grades"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    enrollment_id = Column(Integer, ForeignKey("enrollments.id"), unique=True, nullable=False)
    score = Column(Float, nullable=False)
    letter_grade = Column(String, nullable=True)
    graded_at = Column(DateTime, default=datetime.utcnow)
    graded_by = Column(Integer, ForeignKey("users.id"))

    enrollment = relationship("Enrollment", back_populates="grade")
    grader = relationship("User", foreign_keys=[graded_by])

class Assignment(Base):
    __tablename__ = "assignments"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    due_date = Column(DateTime, nullable=False)
    max_score = Column(Integer, nullable=False)

    course = relationship("Course", back_populates="assignments")
    submissions = relationship("Submission", back_populates="assignment")

class Submission(Base):
    __tablename__ = "submissions"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    assignment_id = Column(Integer, ForeignKey("assignments.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    submitted_at = Column(DateTime, default=datetime.utcnow)
    score = Column(Float, nullable=True)
    status = Column(String, nullable=False, default="submitted")  # submitted, late, rejected
    grader_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    assignment = relationship("Assignment", back_populates="submissions")
    student = relationship("User", back_populates="submissions")
    grader = relationship("User", foreign_keys=[grader_id])