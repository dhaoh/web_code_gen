import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './AuthContext';
import Layout from './pages/Layout';
import Login from './pages/Login';
import UserList from './pages/admin/UserList';
import UserForm from './pages/admin/UserForm';
import DepartmentList from './pages/admin/DepartmentList';
import DepartmentForm from './pages/admin/DepartmentForm';
import CourseList from './pages/CourseList';
import CourseForm from './pages/CourseForm';
import EnrollmentList from './pages/EnrollmentList';
import GradeList from './pages/GradeList';
import GradeForm from './pages/GradeForm';
import AssignmentList from './pages/AssignmentList';
import AssignmentForm from './pages/AssignmentForm';
import SubmissionList from './pages/SubmissionList';
import SubmissionForm from './pages/SubmissionForm';
import MyEnrollments from './pages/MyEnrollments';
import MyGrades from './pages/MyGrades';
import AvailableCourses from './pages/AvailableCourses';

function PrivateRoute({ children, roles }: { children: JSX.Element, roles?: string[] }) {
  const { user } = useAuth();
  if (!user) return <Navigate to="/login" />;
  if (roles && !roles.includes(user.role)) return <Navigate to="/" />;
  return children;
}

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/" element={<Layout />}>
            <Route index element={<div>Welcome to Student Course System</div>} />
            {/* Admin routes */}
            <Route path="users" element={<PrivateRoute roles={['admin']}><UserList /></PrivateRoute>} />
            <Route path="users/new" element={<PrivateRoute roles={['admin']}><UserForm /></PrivateRoute>} />
            <Route path="users/:id/edit" element={<PrivateRoute roles={['admin']}><UserForm /></PrivateRoute>} />
            <Route path="departments" element={<PrivateRoute roles={['admin']}><DepartmentList /></PrivateRoute>} />
            <Route path="departments/new" element={<PrivateRoute roles={['admin']}><DepartmentForm /></PrivateRoute>} />
            <Route path="departments/:id/edit" element={<PrivateRoute roles={['admin']}><DepartmentForm /></PrivateRoute>} />
            {/* Courses - admin/teacher */}
            <Route path="courses" element={<PrivateRoute roles={['admin','teacher']}><CourseList /></PrivateRoute>} />
            <Route path="courses/new" element={<PrivateRoute roles={['admin','teacher']}><CourseForm /></PrivateRoute>} />
            <Route path="courses/:id/edit" element={<PrivateRoute roles={['admin','teacher']}><CourseForm /></PrivateRoute>} />
            {/* Enrollments - admin/teacher/student */}
            <Route path="enrollments" element={<PrivateRoute roles={['admin','teacher','student']}><EnrollmentList /></PrivateRoute>} />
            {/* Grades - teacher/student */}
            <Route path="grades" element={<PrivateRoute roles={['teacher','student']}><GradeList /></PrivateRoute>} />
            <Route path="grades/new" element={<PrivateRoute roles={['teacher']}><GradeForm /></PrivateRoute>} />
            <Route path="grades/:id/edit" element={<PrivateRoute roles={['teacher']}><GradeForm /></PrivateRoute>} />
            {/* Assignments - teacher/student */}
            <Route path="assignments" element={<PrivateRoute roles={['teacher','student']}><AssignmentList /></PrivateRoute>} />
            <Route path="assignments/new" element={<PrivateRoute roles={['teacher']}><AssignmentForm /></PrivateRoute>} />
            <Route path="assignments/:id/edit" element={<PrivateRoute roles={['teacher']}><AssignmentForm /></PrivateRoute>} />
            {/* Submissions */}
            <Route path="submissions" element={<PrivateRoute roles={['teacher','student']}><SubmissionList /></PrivateRoute>} />
            <Route path="submissions/new" element={<PrivateRoute roles={['student']}><SubmissionForm /></PrivateRoute>} />
            {/* Student-specific views */}
            <Route path="my-enrollments" element={<PrivateRoute roles={['student']}><MyEnrollments /></PrivateRoute>} />
            <Route path="my-grades" element={<PrivateRoute roles={['student']}><MyGrades /></PrivateRoute>} />
            <Route path="available-courses" element={<PrivateRoute roles={['student']}><AvailableCourses /></PrivateRoute>} />
          </Route>
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}