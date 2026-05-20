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
        INTEGER,
        primary_key=True,
        autoincrement=True,
    )
    name = Column(
        TEXT,
        nullable=False,
    )
    email = Column(
        TEXT,
        unique=True,
        nullable=False,
    )


class Course(Base):
    __tablename__ = "courses"

    id = Column(
        INTEGER,
        primary_key=True,
        autoincrement=True,
    )
    title = Column(
        TEXT,
        nullable=False,
    )
    description = Column(
        TEXT,
        nullable=True,
    )
    capacity = Column(
        INTEGER,
        nullable=False,
        default=30,
    )


class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(
        INTEGER,
        primary_key=True,
        autoincrement=True,
    )
    student_id = Column(
        INTEGER,
        nullable=False,
    )
    course_id = Column(
        INTEGER,
        nullable=False,
    )
    enrolled_at = Column(
        TEXT,
        nullable=False,
        default=datetime.utcnow,
    )



# Database setup
engine = create_engine("sqlite:///./app.db", echo=False)


def init_db():
    Base.metadata.create_all(engine)


def get_session() -> Session:
    return Session(engine)