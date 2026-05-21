import React from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import StudentsPage from './pages/StudentsPage';
import StudentFormPage from './pages/StudentFormPage';
import CoursesPage from './pages/CoursesPage';
import CourseFormPage from './pages/CourseFormPage';
import EnrollmentsPage from './pages/EnrollmentsPage';
import EnrollmentFormPage from './pages/EnrollmentFormPage';

function App() {
  return (
    <div>
      <nav style={{ padding: '1rem', borderBottom: '1px solid #ccc' }}>
        <Link to="/students" style={{ marginRight: '1rem' }}>Students</Link>
        <Link to="/courses" style={{ marginRight: '1rem' }}>Courses</Link>
        <Link to="/enrollments" style={{ marginRight: '1rem' }}>Enrollments</Link>
      </nav>
      <div style={{ padding: '1rem' }}>
        <Routes>
          <Route path="/" element={<CoursesPage />} />
          <Route path="/students" element={<StudentsPage />} />
          <Route path="/students/new" element={<StudentFormPage />} />
          <Route path="/students/:id/edit" element={<StudentFormPage />} />
          <Route path="/courses" element={<CoursesPage />} />
          <Route path="/courses/new" element={<CourseFormPage />} />
          <Route path="/courses/:id/edit" element={<CourseFormPage />} />
          <Route path="/enrollments" element={<EnrollmentsPage />} />
          <Route path="/enrollments/new" element={<EnrollmentFormPage />} />
        </Routes>
      </div>
    </div>
  );
}

export default App;