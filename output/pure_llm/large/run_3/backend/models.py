from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base
import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)  # 'student','teacher','admin','department_head'
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    major_id = Column(Integer, ForeignKey("majors.id"), nullable=True)
    major = relationship("Major", back_populates="students")
    departments = relationship("Department", back_populates="head_user")
    courses_taught = relationship("Course", back_populates="teacher", foreign_keys="[Course.teacher_id]")
    enrollments = relationship("Enrollment", back_populates="student")

class Department(Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    code = Column(String, unique=True, nullable=False)
    head_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    head_user = relationship("User", back_populates="departments")
    courses = relationship("Course", back_populates="department")
    majors = relationship("Major", back_populates="department")

class Major(Base):
    __tablename__ = "majors"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    code = Column(String, unique=True, nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    department = relationship("Department", back_populates="majors")
    total_credits_required = Column(Integer, nullable=False)
    students = relationship("User", back_populates="major")
    required_courses_link = relationship("MajorCourse", back_populates="major")

class MajorCourse(Base):
    __tablename__ = "major_courses"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    major_id = Column(Integer, ForeignKey("majors.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    major = relationship("Major", back_populates="required_courses_link")
    course = relationship("Course", back_populates="required_by_majors")

class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
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
    schedules = relationship("CourseSchedule", back_populates="course")
    enrollments = relationship("Enrollment", back_populates="course")
    prerequisites_of = relationship("Prerequisite", back_populates="course", foreign_keys="[Prerequisite.course_id]")
    prerequisite_for = relationship("Prerequisite", back_populates="prerequisite_course", foreign_keys="[Prerequisite.prerequisite_course_id]")
    assignments = relationship("Assignment", back_populates="course")
    required_by_majors = relationship("MajorCourse", back_populates="course")

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
    day_of_week = Column(Integer, nullable=False)  # 0=Monday, 6=Sunday
    start_time = Column(String, nullable=False)   # format "HH:MM"
    end_time = Column(String, nullable=False)
    course_schedules = relationship("CourseSchedule", back_populates="schedule")

class CourseSchedule(Base):
    __tablename__ = "course_schedules"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    schedule_id = Column(Integer, ForeignKey("schedules.id"), nullable=False)
    course = relationship("Course", back_populates="schedules")
    schedule = relationship("Schedule", back_populates="course_schedules")

class Enrollment(Base):
    __tablename__ = "enrollments"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    enrolled_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    status = Column(String, nullable=False)  # 'enrolled','completed','dropped'
    student = relationship("User", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")
    grade = relationship("Grade", uselist=False, back_populates="enrollment")

class Grade(Base):
    __tablename__ = "grades"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    enrollment_id = Column(Integer, ForeignKey("enrollments.id"), unique=True, nullable=False)
    score = Column(Float, nullable=False)
    letter_grade = Column(String, nullable=True)
    graded_at = Column(DateTime, default=datetime.datetime.utcnow)
    graded_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    enrollment = relationship("Enrollment", back_populates="grade")

class Assignment(Base):
    __tablename__ = "assignments"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    due_date = Column(DateTime, nullable=False)
    max_score = Column(Integer, nullable=False)
    course = relationship("Course", back_populates="assignments")
    submissions = relationship("AssignmentSubmission", back_populates="assignment")

class AssignmentSubmission(Base):
    __tablename__ = "assignment_submissions"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    assignment_id = Column(Integer, ForeignKey("assignments.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    submitted_at = Column(DateTime, default=datetime.datetime.utcnow)
    content = Column(String, nullable=True)  # simple text content
    score = Column(Float, nullable=True)
    late_penalty_applied = Column(Boolean, default=False)
    assignment = relationship("Assignment", back_populates="submissions")

class Prerequisite(Base):
    __tablename__ = "prerequisites"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    prerequisite_course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    is_mandatory = Column(Boolean, nullable=False)
    course = relationship("Course", back_populates="prerequisites_of", foreign_keys=[course_id])
    prerequisite_course = relationship("Course", back_populates="prerequisite_for", foreign_keys=[prerequisite_course_id])
    __table_args__ = (UniqueConstraint('course_id', 'prerequisite_course_id', name='unique_prereq'),)