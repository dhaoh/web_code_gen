"""
Database models for student_course_system_medium.
Generated from model definition.
"""
from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Column, Integer, String, Float, Boolean, DateTime,
    ForeignKey, create_engine, UniqueConstraint
)
from sqlalchemy.orm import DeclarativeBase, relationship, Session


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    username = Column(
        String,
        unique=True,
        nullable=False,
    )
    password_hash = Column(
        String,
        nullable=False,
    )
    role = Column(
        String,
        nullable=False,
    )
    full_name = Column(
        String,
        nullable=False,
    )
    email = Column(
        String,
        unique=True,
        nullable=False,
    )


class Department(Base):
    __tablename__ = "departments"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    name = Column(
        String,
        unique=True,
        nullable=False,
    )
    code = Column(
        String,
        unique=True,
        nullable=False,
    )


class Course(Base):
    __tablename__ = "courses"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    title = Column(
        String,
        nullable=False,
    )
    description = Column(
        String,
        nullable=True,
    )
    capacity = Column(
        Integer,
        nullable=False,
        default=30,
    )
    credits = Column(
        Integer,
        nullable=False,
        default=3,
    )
    department_id = Column(
        Integer,
        nullable=False,
    )

    # Relationship: Course -> Department
    # Relationship: Course -> User

class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    student_id = Column(
        Integer,
        nullable=False,
    )
    course_id = Column(
        Integer,
        nullable=False,
    )
    enrolled_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )


class Grade(Base):
    __tablename__ = "grades"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    enrollment_id = Column(
        Integer,
        unique=True,
        nullable=False,
    )
    score = Column(
        Float,
        nullable=False,
    )
    letter_grade = Column(
        String,
        nullable=True,
    )
    graded_at = Column(
        DateTime,
        nullable=True,
    )


class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    course_id = Column(
        Integer,
        nullable=False,
    )
    title = Column(
        String,
        nullable=False,
    )
    description = Column(
        String,
        nullable=True,
    )
    due_date = Column(
        DateTime,
        nullable=False,
    )
    max_score = Column(
        Integer,
        nullable=False,
        default=100,
    )

    # Relationship: Assignment -> Course


# Database setup
engine = create_engine("sqlite:///./app.db", echo=False)


def init_db():
    Base.metadata.create_all(engine)


def get_session() -> Session:
    return Session(engine)
