import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, Navigate } from 'react-router-dom';
import StudentsListPage from './pages/StudentsListPage';
import StudentFormPage from './pages/StudentFormPage';
import CoursesListPage from './pages/CoursesListPage';
import CourseFormPage from './pages/CourseFormPage';
import EnrollmentsListPage from './pages/EnrollmentsListPage';
import EnrollmentFormPage from './pages/EnrollmentFormPage';

const App: React.FC = () => {
  return (
    <Router>
      <div style={styles.container}>
        <nav style={styles.nav}>
          <h1 style={styles.title}>Student Course System</h1>
          <div style={styles.navLinks}>
            <Link to="/students" style={styles.navLink}>Students</Link>
            <Link to="/courses" style={styles.navLink}>Courses</Link>
            <Link to="/enrollments" style={styles.navLink}>Enrollments</Link>
          </div>
        </nav>
        <main style={styles.main}>
          <Routes>
            <Route path="/" element={<Navigate to="/students" replace />} />
            <Route path="/students" element={<StudentsListPage />} />
            <Route path="/students/new" element={<StudentFormPage />} />
            <Route path="/students/:id/edit" element={<StudentFormPage />} />
            <Route path="/courses" element={<CoursesListPage />} />
            <Route path="/courses/new" element={<CourseFormPage />} />
            <Route path="/courses/:id/edit" element={<CourseFormPage />} />
            <Route path="/enrollments" element={<EnrollmentsListPage />} />
            <Route path="/enrollments/new" element={<EnrollmentFormPage />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
};

const styles: { [key: string]: React.CSSProperties } = {
  container: {
    fontFamily: 'Arial, sans-serif',
    maxWidth: '1200px',
    margin: '0 auto',
    padding: '20px',
  },
  nav: {
    backgroundColor: '#f8f9fa',
    padding: '20px',
    borderRadius: '8px',
    marginBottom: '20px',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
  },
  title: {
    margin: '0 0 15px 0',
    color: '#333',
    fontSize: '24px',
  },
  navLinks: {
    display: 'flex',
    gap: '20px',
  },
  navLink: {
    textDecoration: 'none',
    color: '#007bff',
    fontSize: '16px',
    fontWeight: 'bold',
    padding: '8px 16px',
    borderRadius: '4px',
    transition: 'background-color 0.3s',
  },
  main: {
    backgroundColor: 'white',
    padding: '20px',
    borderRadius: '8px',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
  },
};

export default App;