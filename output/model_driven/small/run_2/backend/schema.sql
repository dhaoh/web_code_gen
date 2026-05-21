-- Generated from model: student_course_system_small
-- A simple student course selection system. Students can browse available courses and enroll. The system tracks enrollments and prevents over-capacity enrollment.

-- Generation timestamp: 2026-05-21T13:36:11.111040+00:00

-- ==========================================
-- Table: students
-- ==========================================
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
);

-- ==========================================
-- Table: courses
-- ==========================================
CREATE TABLE IF NOT EXISTS courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT DEFAULT NULL,
    capacity INTEGER NOT NULL DEFAULT 30
);

-- ==========================================
-- Table: enrollments
-- ==========================================
CREATE TABLE IF NOT EXISTS enrollments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    enrolled_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ==========================================
-- Foreign Key Constraints
-- ==========================================

-- ==========================================
-- Junction Tables (Many-to-Many)
-- ==========================================
-- Junction table 'Enrollments' already handled in entity definition above.
-- Junction table 'Enrollments' already handled in entity definition above.
