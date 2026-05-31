"""
FastAPI routers for the student_course_system_large application.
"""

from user_routes import router as users_router
from departments_routes import router as departments_router
from majors_routes import router as majors_router
from courses_routes import router as courses_router
from prerequisites_routes import router as prerequisites_router
from classrooms_routes import router as classrooms_router
from schedules_routes import router as schedules_router
from courseschedules_routes import router as courseschedules_router
from enrollments_routes import router as enrollments_router
from grades_routes import router as grades_router
from assignments_routes import router as assignments_router

routers = [
    users_router,
    departments_router,
    majors_router,
    courses_router,
    prerequisites_router,
    classrooms_router,
    schedules_router,
    courseschedules_router,
    enrollments_router,
    grades_router,
    assignments_router,
]