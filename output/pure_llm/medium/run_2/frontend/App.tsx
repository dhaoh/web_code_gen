import React from 'react';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import UserListPage from './pages/UserListPage';
import UserFormPage from './pages/UserFormPage';
import DepartmentListPage from './pages/DepartmentListPage';
import DepartmentFormPage from './pages/DepartmentFormPage';
import CourseListPage from './pages/CourseListPage';
import CourseFormPage from './pages/CourseFormPage';
import EnrollmentListPage from './pages/EnrollmentListPage';
import EnrollmentFormPage from './pages/EnrollmentFormPage';
import GradeListPage from './pages/GradeListPage';
import GradeFormPage from './pages/GradeFormPage';
import AssignmentListPage from './pages/AssignmentListPage';
import AssignmentFormPage from './pages/AssignmentFormPage';

const Navbar = () => (
  <nav style={{ background: '#eee', padding: '1rem' }}>
    <Link to="/users" style={{ marginRight: '1rem' }}>Users</Link>
    <Link to="/departments" style={{ marginRight: '1rem' }}>Departments</Link>
    <Link to="/courses" style={{ marginRight: '1rem' }}>Courses</Link>
    <Link to="/enrollments" style={{ marginRight: '1rem' }}>Enrollments</Link>
    <Link to="/grades" style={{ marginRight: '1rem' }}>Grades</Link>
    <Link to="/assignments" style={{ marginRight: '1rem' }}>Assignments</Link>
  </nav>
);

function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <div className="container" style={{ padding: '2rem' }}>
        <Routes>
          <Route path="/users" element={<UserListPage />} />
          <Route path="/users/new" element={<UserFormPage />} />
          <Route path="/users/:id/edit" element={<UserFormPage />} />
          <Route path="/departments" element={<DepartmentListPage />} />
          <Route path="/departments/new" element={<DepartmentFormPage />} />
          <Route path="/departments/:id/edit" element={<DepartmentFormPage />} />
          <Route path="/courses" element={<CourseListPage />} />
          <Route path="/courses/new" element={<CourseFormPage />} />
          <Route path="/courses/:id/edit" element={<CourseFormPage />} />
          <Route path="/enrollments" element={<EnrollmentListPage />} />
          <Route path="/enrollments/new" element={<EnrollmentFormPage />} />
          <Route path="/enrollments/:id/edit" element={<EnrollmentFormPage />} />
          <Route path="/grades" element={<GradeListPage />} />
          <Route path="/grades/new" element={<GradeFormPage />} />
          <Route path="/grades/:id/edit" element={<GradeFormPage />} />
          <Route path="/assignments" element={<AssignmentListPage />} />
          <Route path="/assignments/new" element={<AssignmentFormPage />} />
          <Route path="/assignments/:id/edit" element={<AssignmentFormPage />} />
          <Route path="/" element={<h1>Welcome to Student Course System</h1>} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;