import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import StudentListPage from './pages/StudentListPage';
import StudentFormPage from './pages/StudentFormPage';
import CourseListPage from './pages/CourseListPage';
import CourseFormPage from './pages/CourseFormPage';
import EnrollmentListPage from './pages/EnrollmentListPage';
import EnrollmentFormPage from './pages/EnrollmentFormPage';

const App: React.FC = () => {
  return (
    <Router>
      <div>
        <nav>
          <ul>
            <li><Link to="/students">Students</Link></li>
            <li><Link to="/courses">Courses</Link></li>
            <li><Link to="/enrollments">Enrollments</Link></li>
          </ul>
        </nav>
        <hr />
        <Routes>
          <Route path="/students" element={<StudentListPage />} />
          <Route path="/students/new" element={<StudentFormPage />} />
          <Route path="/students/:id/edit" element={<StudentFormPage />} />
          <Route path="/courses" element={<CourseListPage />} />
          <Route path="/courses/new" element={<CourseFormPage />} />
          <Route path="/courses/:id/edit" element={<CourseFormPage />} />
          <Route path="/enrollments" element={<EnrollmentListPage />} />
          <Route path="/enrollments/new" element={<EnrollmentFormPage />} />
          <Route path="/" element={<div>Welcome to Student Course System. Select a section above.</div>} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;