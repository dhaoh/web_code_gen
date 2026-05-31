-- Generated from model: student_course_system_medium
-- A complete student course selection and management system with users, departments, courses, enrollments, and grades. Teachers manage courses, students enroll and receive grades.

-- Generation timestamp: 2026-05-24T13:53:51.914035+00:00

-- ==========================================
-- Table: users
-- ==========================================
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
);

-- ==========================================
-- Table: departments
-- ==========================================
CREATE TABLE IF NOT EXISTS departments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    code TEXT UNIQUE NOT NULL
);

-- ==========================================
-- Table: courses
-- ==========================================
CREATE TABLE IF NOT EXISTS courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT DEFAULT NULL,
    capacity INTEGER NOT NULL DEFAULT 30,
    credits INTEGER NOT NULL DEFAULT 3,
    department_id INTEGER NOT NULL
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
-- Table: grades
-- ==========================================
CREATE TABLE IF NOT EXISTS grades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    enrollment_id INTEGER UNIQUE NOT NULL,
    score REAL NOT NULL,
    letter_grade TEXT DEFAULT NULL,
    graded_at TEXT DEFAULT NULL
);

-- ==========================================
-- Table: assignments
-- ==========================================
CREATE TABLE IF NOT EXISTS assignments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT DEFAULT NULL,
    due_date TEXT NOT NULL,
    max_score INTEGER NOT NULL DEFAULT 100
);

-- ==========================================
-- Foreign Key Constraints
-- ==========================================
-- Course.department_id -> Departments
-- ALTER TABLE courses ADD CONSTRAINT fk_courses_department_id
--     FOREIGN KEY (department_id) REFERENCES Departments(id);
-- Course.teacher_id -> Users
-- ALTER TABLE courses ADD CONSTRAINT fk_courses_teacher_id
--     FOREIGN KEY (teacher_id) REFERENCES Users(id);
-- Assignment.course_id -> Courses
-- ALTER TABLE assignments ADD CONSTRAINT fk_assignments_course_id
--     FOREIGN KEY (course_id) REFERENCES Courses(id);

-- ==========================================
-- Junction Tables (Many-to-Many)
-- ==========================================
-- Junction table 'Enrollments' already handled in entity definition above.
