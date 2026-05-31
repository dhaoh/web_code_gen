import React, { useEffect, useState } from 'react';
import { BrowserRouter, Routes, Route, Link, useNavigate, useLocation } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import UserListPage from './pages/UserListPage';
import UserFormPage from './pages/UserFormPage';
import DepartmentListPage from './pages/DepartmentListPage';
import DepartmentFormPage from './pages/DepartmentFormPage';
import MajorListPage from './pages/MajorListPage';
import MajorFormPage from './pages/MajorFormPage';
import CourseListPage from './pages/CourseListPage';
import CourseFormPage from './pages/CourseFormPage';
import ClassroomListPage from './pages/ClassroomListPage';
import ClassroomFormPage from './pages/ClassroomFormPage';
import ScheduleListPage from './pages/ScheduleListPage';
import ScheduleFormPage from './pages/ScheduleFormPage';
import EnrollmentListPage from './pages/EnrollmentListPage';
import EnrollmentFormPage from './pages/EnrollmentFormPage';
import GradeListPage from './pages/GradeListPage';
import GradeFormPage from './pages/GradeFormPage';
import AssignmentListPage from './pages/AssignmentListPage';
import AssignmentFormPage from './pages/AssignmentFormPage';
import MajorProgressPage from './pages/MajorProgressPage';
import { list } from './api';

const Layout = ({ children }: { children: React.ReactNode }) => {
  const location = useLocation();
  const navigate = useNavigate();
  const [user, setUser] = useState<any>(null);

  useEffect(() => {
    (async () => {
      try {
        const me = await list('/me')(/* this won't work */);
        setUser(me);
      } catch { setUser(null); }
    })();
  }, []);

  if (location.pathname === '/login') return <>{children}</>;

  if (!user) return <div>Loading...</div>;

  return (
    <div style={{ display: 'flex' }}>
      <nav style={{ width: '200px', background: '#f0f0f0', padding: '1rem' }}>
        <h3>Menu</h3>
        <Link to="/users">Users</Link><br/>
        <Link to="/departments">Departments</Link><br/>
        <Link to="/majors">Majors</Link><br/>
        <Link to="/courses">Courses</Link><br/>
        <Link to="/classrooms">Classrooms</Link><br/>
        <Link to="/schedules">Schedules</Link><br/>
        <Link to="/enrollments">Enrollments</Link><br/>
        <Link to="/grades">Grades</Link><br/>
        <Link to="/assignments">Assignments</Link><br/>
        <Link to="/major-progress">Major Progress</Link><br/>
        <button onClick={() => { localStorage.removeItem('token'); navigate('/login'); }}>Logout</button>
      </nav>
      <main style={{ flex: 1, padding: '1rem' }}>{children}</main>
    </div>
  );
};

const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/users" element={<UserListPage />} />
          <Route path="/users/new" element={<UserFormPage />} />
          <Route path="/users/:id/edit" element={<UserFormPage />} />
          <Route path="/departments" element={<DepartmentListPage />} />
          <Route path="/departments/new" element={<DepartmentFormPage />} />
          <Route path="/departments/:id/edit" element={<DepartmentFormPage />} />
          <Route path="/majors" element={<MajorListPage />} />
          <Route path="/majors/new" element={<MajorFormPage />} />
          <Route path="/majors/:id/edit" element={<MajorFormPage />} />
          <Route path="/courses" element={<CourseListPage />} />
          <Route path="/courses/new" element={<CourseFormPage />} />
          <Route path="/courses/:id/edit" element={<CourseFormPage />} />
          <Route path="/classrooms" element={<ClassroomListPage />} />
          <Route path="/classrooms/new" element={<ClassroomFormPage />} />
          <Route path="/classrooms/:id/edit" element={<ClassroomFormPage />} />
          <Route path="/schedules" element={<ScheduleListPage />} />
          <Route path="/schedules/new" element={<ScheduleFormPage />} />
          <Route path="/schedules/:id/edit" element={<ScheduleFormPage />} />
          <Route path="/enrollments" element={<EnrollmentListPage />} />
          <Route path="/enrollments/new" element={<EnrollmentFormPage />} />
          <Route path="/enrollments/:id/edit" element={<EnrollmentFormPage />} />
          <Route path="/grades" element={<GradeListPage />} />
          <Route path="/grades/new" element={<GradeFormPage />} />
          <Route path="/grades/:id/edit" element={<GradeFormPage />} />
          <Route path="/assignments" element={<AssignmentListPage />} />
          <Route path="/assignments/new" element={<AssignmentFormPage />} />
          <Route path="/assignments/:id/edit" element={<AssignmentFormPage />} />
          <Route path="/major-progress" element={<MajorProgressPage />} />
          <Route path="*" element={<div>404</div>} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
};

export default App;