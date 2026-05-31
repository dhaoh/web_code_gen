import React from 'react';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import StudentListPage from './pages/StudentListPage';
import StudentFormPage from './pages/StudentFormPage';
import CourseListPage from './pages/CourseListPage';
import CourseFormPage from './pages/CourseFormPage';
import EnrollmentListPage from './pages/EnrollmentListPage';
import EnrollmentFormPage from './pages/EnrollmentFormPage';

const App: React.FC = () => {
  return (
    <BrowserRouter>
      <nav style={{ padding: '1rem', borderBottom: '1px solid #ccc' }}>
        <Link to="/students" style={{ marginRight: '1rem' }}>Students</Link>
        <Link to="/courses" style={{ marginRight: '1rem' }}>Courses</Link>
        <Link to="/enrollments">Enrollments</Link>
      </nav>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/students" element={<StudentListPage />} />
        <Route path="/students/new" element={<StudentFormPage />} />
        <Route path="/students/:id/edit" element={<StudentFormPage />} />
        <Route path="/courses" element={<CourseListPage />} />
        <Route path="/courses/new" element={<CourseFormPage />} />
        <Route path="/courses/:id/edit" element={<CourseFormPage />} />
        <Route path="/enrollments" element={<EnrollmentListPage />} />
        <Route path="/enrollments/new" element={<EnrollmentFormPage />} />
      </Routes>
    </BrowserRouter>
  );
};

const Home: React.FC = () => <h2>Welcome to Student Course System</h2>;

export default App;