"""
Database models for student_course_system_small.
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


class Student(Base):
    __tablename__ = "students"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    name = Column(
        String,
        nullable=False,
    )
    email = Column(
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



# Database setup
engine = create_engine("sqlite:///./app.db", echo=False)


def init_db():
    Base.metadata.create_all(engine)


def get_session() -> Session:
    return Session(engine)
