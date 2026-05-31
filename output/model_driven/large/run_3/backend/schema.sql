-- Generated from model: student_course_system_large
-- A comprehensive university course management system with users, departments, programs, courses, prerequisites, classrooms, schedules, enrollments, grades, and assignments.

-- Generation timestamp: 2026-05-24T14:52:41.046575+00:00

-- ==========================================
-- Table: users
-- ==========================================
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    major_id INTEGER DEFAULT NULL
);

-- ==========================================
-- Table: departments
-- ==========================================
CREATE TABLE IF NOT EXISTS departments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    code TEXT UNIQUE NOT NULL,
    head_user_id INTEGER DEFAULT NULL
);

-- ==========================================
-- Table: majors
-- ==========================================
CREATE TABLE IF NOT EXISTS majors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    code TEXT UNIQUE NOT NULL,
    department_id INTEGER NOT NULL,
    total_credits_required INTEGER NOT NULL DEFAULT 120
);

-- ==========================================
-- Table: courses
-- ==========================================
CREATE TABLE IF NOT EXISTS courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    code TEXT UNIQUE NOT NULL,
    description TEXT DEFAULT NULL,
    capacity INTEGER NOT NULL DEFAULT 30,
    credits INTEGER NOT NULL DEFAULT 3,
    department_id INTEGER NOT NULL,
    teacher_id INTEGER NOT NULL,
    classroom_id INTEGER DEFAULT NULL,
    semester TEXT NOT NULL
);

-- ==========================================
-- Table: prerequisites
-- ==========================================
CREATE TABLE IF NOT EXISTS prerequisites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id INTEGER NOT NULL,
    prerequisite_course_id INTEGER NOT NULL,
    is_mandatory INTEGER NOT NULL DEFAULT True
);

-- ==========================================
-- Table: classrooms
-- ==========================================
CREATE TABLE IF NOT EXISTS classrooms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    building TEXT NOT NULL,
    room_number TEXT NOT NULL,
    capacity INTEGER NOT NULL
);

-- ==========================================
-- Table: schedules
-- ==========================================
CREATE TABLE IF NOT EXISTS schedules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    day_of_week INTEGER NOT NULL,
    start_time TEXT NOT NULL,
    end_time TEXT NOT NULL
);

-- ==========================================
-- Table: courseschedules
-- ==========================================
CREATE TABLE IF NOT EXISTS courseschedules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id INTEGER NOT NULL,
    schedule_id INTEGER NOT NULL
);

-- ==========================================
-- Table: enrollments
-- ==========================================
CREATE TABLE IF NOT EXISTS enrollments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    enrolled_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status TEXT NOT NULL DEFAULT active
);

-- ==========================================
-- Table: grades
-- ==========================================
CREATE TABLE IF NOT EXISTS grades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    enrollment_id INTEGER UNIQUE NOT NULL,
    score REAL NOT NULL,
    letter_grade TEXT DEFAULT NULL,
    graded_at TEXT DEFAULT NULL,
    graded_by INTEGER DEFAULT NULL
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
-- User.major_id -> Majors
-- ALTER TABLE users ADD CONSTRAINT fk_users_major_id
--     FOREIGN KEY (major_id) REFERENCES Majors(id);
-- Department.head_user_id -> Users
-- ALTER TABLE departments ADD CONSTRAINT fk_departments_head_user_id
--     FOREIGN KEY (head_user_id) REFERENCES Users(id);
-- Major.department_id -> Departments
-- ALTER TABLE majors ADD CONSTRAINT fk_majors_department_id
--     FOREIGN KEY (department_id) REFERENCES Departments(id);
-- Course.department_id -> Departments
-- ALTER TABLE courses ADD CONSTRAINT fk_courses_department_id
--     FOREIGN KEY (department_id) REFERENCES Departments(id);
-- Course.teacher_id -> Users
-- ALTER TABLE courses ADD CONSTRAINT fk_courses_teacher_id
--     FOREIGN KEY (teacher_id) REFERENCES Users(id);
-- Course.classroom_id -> Classrooms
-- ALTER TABLE courses ADD CONSTRAINT fk_courses_classroom_id
--     FOREIGN KEY (classroom_id) REFERENCES Classrooms(id);

-- ==========================================
-- Junction Tables (Many-to-Many)
-- ==========================================
-- Junction table 'Enrollments' already handled in entity definition above.
-- Junction table 'CourseSchedules' already handled in entity definition above.
