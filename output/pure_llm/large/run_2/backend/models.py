from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base
import datetime

course_schedules = Table(
    "course_schedules",
    Base.metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("course_id", Integer, ForeignKey("courses.id")),
    Column("schedule_id", Integer, ForeignKey("schedules.id"))
)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)  # student, teacher, admin, department_head
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    major_id = Column(Integer, ForeignKey("majors.id"), nullable=True)
    major = relationship("Major", backref="students")
    courses_taught = relationship("Course", back_populates="teacher")
    enrollments = relationship("Enrollment", back_populates="student")
    grades_given = relationship("Grade", back_populates="graded_by_user")
    submissions = relationship("Submission", back_populates="student")

class Department(Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    code = Column(String, unique=True, nullable=False)
    head_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    head = relationship("User", backref="headed_departments")
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
    semester = Column(String, nullable=False)  # e.g. "Fall2023"
    department = relationship("Department", back_populates="courses")
    teacher = relationship("User", back_populates="courses_taught")
    classroom = relationship("Classroom", back_populates="courses")
    schedules = relationship("Schedule", secondary=course_schedules, back_populates="courses")
    prerequisites = relationship("Prerequisite", back_populates="course", foreign_keys="[Prerequisite.course_id]")
    requisite_for = relationship("Prerequisite", back_populates="prerequisite_course", foreign_keys="[Prerequisite.prerequisite_course_id]")
    enrollments = relationship("Enrollment", back_populates="course")
    assignments = relationship("Assignment", back_populates="course")
    major_required = relationship("MajorCourse", back_populates="course")

class Prerequisite(Base):
    __tablename__ = "prerequisites"
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    prerequisite_course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    is_mandatory = Column(Boolean, nullable=False)
    course = relationship("Course", back_populates="prerequisites", foreign_keys=[course_id])
    prerequisite_course = relationship("Course", back_populates="requisite_for", foreign_keys=[prerequisite_course_id])

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
    day_of_week = Column(Integer, nullable=False)  # 0=Monday..6=Sunday
    start_time = Column(String, nullable=False)     # HH:MM
    end_time = Column(String, nullable=False)       # HH:MM
    courses = relationship("Course", secondary=course_schedules, back_populates="schedules")

class Enrollment(Base):
    __tablename__ = "enrollments"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    enrolled_at = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String, nullable=False)  # enrolled, completed, dropped
    student = relationship("User", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")
    grade = relationship("Grade", uselist=False, back_populates="enrollment")

class Grade(Base):
    __tablename__ = "grades"
    id = Column(Integer, primary_key=True, index=True)
    enrollment_id = Column(Integer, ForeignKey("enrollments.id"), unique=True, nullable=False)
    score = Column(Float, nullable=False)
    letter_grade = Column(String, nullable=True)
    graded_at = Column(DateTime, nullable=True)
    graded_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    enrollment = relationship("Enrollment", back_populates="grade")
    graded_by_user = relationship("User", back_populates="grades_given")

class Assignment(Base):
    __tablename__ = "assignments"
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    due_date = Column(DateTime, nullable=False)
    max_score = Column(Integer, nullable=False)
    course = relationship("Course", back_populates="assignments")
    submissions = relationship("Submission", back_populates="assignment")

class Submission(Base):
    __tablename__ = "submissions"
    id = Column(Integer, primary_key=True, index=True)
    assignment_id = Column(Integer, ForeignKey("assignments.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    submitted_at = Column(DateTime, default=datetime.datetime.utcnow)
    score = Column(Float, nullable=True)
    late = Column(Boolean, default=False)
    assignment = relationship("Assignment", back_populates="submissions")
    student = relationship("User", back_populates="submissions")

class MajorCourse(Base):
    __tablename__ = "major_courses"
    id = Column(Integer, primary_key=True, index=True)
    major_id = Column(Integer, ForeignKey("majors.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    required = Column(Boolean, default=True)
    major = relationship("Major", backref="major_courses")
    course = relationship("Course", back_populates="major_required")