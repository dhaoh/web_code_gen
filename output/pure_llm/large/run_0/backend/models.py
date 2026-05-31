from sqlalchemy import (
    Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Table, Text
)
from sqlalchemy.orm import relationship
from .database import Base
import datetime

# Association table for Course <-> Schedule many-to-many
course_schedule_table = Table(
    "course_schedule",
    Base.metadata,
    Column("id", Integer, primary_key=True, index=True, autoincrement=True),
    Column("course_id", Integer, ForeignKey("courses.id")),
    Column("schedule_id", Integer, ForeignKey("schedules.id"))
)

# Association table for Major <-> Course many-to-many for major requirements
major_courses_table = Table(
    "major_courses",
    Base.metadata,
    Column("id", Integer, primary_key=True, index=True, autoincrement=True),
    Column("major_id", Integer, ForeignKey("majors.id")),
    Column("course_id", Integer, ForeignKey("courses.id"))
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)  # "student", "teacher", "admin", "department_head"
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    major_id = Column(Integer, ForeignKey("majors.id"), nullable=True)
    
    # Relationships
    major = relationship("Major", back_populates="students")
    taught_courses = relationship("Course", back_populates="teacher", foreign_keys="Course.teacher_id")
    headed_department = relationship("Department", back_populates="head", foreign_keys="Department.head_user_id")
    enrollments = relationship("Enrollment", back_populates="student")
    grades_given = relationship("Grade", back_populates="grader", foreign_keys="Grade.graded_by")
    submissions = relationship("AssignmentSubmission", back_populates="student")

    def __repr__(self):
        return f"<User {self.username}>"

class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    code = Column(String, unique=True, nullable=False)
    head_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    head = relationship("User", back_populates="headed_department", foreign_keys=[head_user_id])
    courses = relationship("Course", back_populates="department")
    majors = relationship("Major", back_populates="department")

    def __repr__(self):
        return f"<Department {self.code}>"

class Major(Base):
    __tablename__ = "majors"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    code = Column(String, unique=True, nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    total_credits_required = Column(Integer, nullable=False)
    
    department = relationship("Department", back_populates="majors")
    students = relationship("User", back_populates="major")
    required_courses = relationship("Course", secondary=major_courses_table, back_populates="majors")

    def __repr__(self):
        return f"<Major {self.code}>"

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
    
    # Relationships
    department = relationship("Department", back_populates="courses")
    teacher = relationship("User", back_populates="taught_courses", foreign_keys=[teacher_id])
    classroom = relationship("Classroom", back_populates="courses")
    schedules = relationship("Schedule", secondary=course_schedule_table, back_populates="courses")
    prerequisites_as_course = relationship("Prerequisite", back_populates="course", foreign_keys="Prerequisite.course_id")
    prerequisites_as_prereq = relationship("Prerequisite", back_populates="prerequisite_course", foreign_keys="Prerequisite.prerequisite_course_id")
    enrollments = relationship("Enrollment", back_populates="course")
    assignments = relationship("Assignment", back_populates="course")
    majors = relationship("Major", secondary=major_courses_table, back_populates="required_courses")

    def __repr__(self):
        return f"<Course {self.code}>"

class Prerequisite(Base):
    __tablename__ = "prerequisites"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    prerequisite_course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    is_mandatory = Column(Boolean, nullable=False, default=True)
    
    course = relationship("Course", back_populates="prerequisites_as_course", foreign_keys=[course_id])
    prerequisite_course = relationship("Course", back_populates="prerequisites_as_prereq", foreign_keys=[prerequisite_course_id])

    def __repr__(self):
        return f"<Prerequisite {self.id}>"

class Classroom(Base):
    __tablename__ = "classrooms"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    building = Column(String, nullable=False)
    room_number = Column(String, nullable=False)
    capacity = Column(Integer, nullable=False)
    
    courses = relationship("Course", back_populates="classroom")

    def __repr__(self):
        return f"<Classroom {self.building}-{self.room_number}>"

class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    day_of_week = Column(Integer, nullable=False)  # 0=Monday, 6=Sunday
    start_time = Column(String, nullable=False)  # "HH:MM"
    end_time = Column(String, nullable=False)    # "HH:MM"
    
    courses = relationship("Course", secondary=course_schedule_table, back_populates="schedules")

    def __repr__(self):
        return f"<Schedule day={self.day_of_week} {self.start_time}-{self.end_time}>"

class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    enrolled_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    status = Column(String, nullable=False, default="active")  # active, completed, dropped
    
    student = relationship("User", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")
    grade = relationship("Grade", uselist=False, back_populates="enrollment")

    def __repr__(self):
        return f"<Enrollment student={self.student_id} course={self.course_id}>"

class Grade(Base):
    __tablename__ = "grades"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    enrollment_id = Column(Integer, ForeignKey("enrollments.id"), unique=True, nullable=False)
    score = Column(Float, nullable=False)
    letter_grade = Column(String, nullable=True)
    graded_at = Column(DateTime, nullable=True)
    graded_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    enrollment = relationship("Enrollment", back_populates="grade")
    grader = relationship("User", back_populates="grades_given", foreign_keys=[graded_by])

    def __repr__(self):
        return f"<Grade enrollment={self.enrollment_id} score={self.score}>"

class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    due_date = Column(DateTime, nullable=False)
    max_score = Column(Integer, nullable=False)
    
    course = relationship("Course", back_populates="assignments")
    submissions = relationship("AssignmentSubmission", back_populates="assignment")

    def __repr__(self):
        return f"<Assignment {self.title}>"

class AssignmentSubmission(Base):
    __tablename__ = "assignment_submissions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    assignment_id = Column(Integer, ForeignKey("assignments.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    submitted_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    score = Column(Float, nullable=True)
    status = Column(String, nullable=False, default="submitted")  # submitted, late, rejected
    
    assignment = relationship("Assignment", back_populates="submissions")
    student = relationship("User", back_populates="submissions")

    def __repr__(self):
        return f"<Submission assignment={self.assignment_id} student={self.student_id}>"