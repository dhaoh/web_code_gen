import React, { useEffect, useState } from "react";
import { BrowserRouter, Routes, Route, Link, useNavigate } from "react-router-dom";
import { api } from "./api";
import LoginPage from "./pages/LoginPage";
import UserListPage from "./pages/UserListPage";
import UserFormPage from "./pages/UserFormPage";
import DepartmentListPage from "./pages/DepartmentListPage";
import DepartmentFormPage from "./pages/DepartmentFormPage";
import MajorListPage from "./pages/MajorListPage";
import MajorFormPage from "./pages/MajorFormPage";
import CourseListPage from "./pages/CourseListPage";
import CourseFormPage from "./pages/CourseFormPage";
import PrerequisiteListPage from "./pages/PrerequisiteListPage";
import PrerequisiteFormPage from "./pages/PrerequisiteFormPage";
import ClassroomListPage from "./pages/ClassroomListPage";
import ClassroomFormPage from "./pages/ClassroomFormPage";
import ScheduleListPage from "./pages/ScheduleListPage";
import ScheduleFormPage from "./pages/ScheduleFormPage";
import EnrollmentListPage from "./pages/EnrollmentListPage";
import EnrollmentFormPage from "./pages/EnrollmentFormPage";
import GradeListPage from "./pages/GradeListPage";
import GradeFormPage from "./pages/GradeFormPage";
import AssignmentListPage from "./pages/AssignmentListPage";
import AssignmentFormPage from "./pages/AssignmentFormPage";

function App() {
  const [logged, setLogged] = useState(!!api.getToken());
  const navigate = useNavigate();

  useEffect(() => {
    if (!logged) navigate("/login");
  }, [logged]);

  const handleLogin = (token: string) => {
    api.setToken(token);
    setLogged(true);
    navigate("/");
  };

  const handleLogout = () => {
    api.setToken(null);
    setLogged(false);
    navigate("/login");
  };

  return (
    <div>
      <nav>
        {logged ? (
          <>
            <Link to="/users">Users</Link> |{" "}
            <Link to="/departments">Departments</Link> |{" "}
            <Link to="/majors">Majors</Link> |{" "}
            <Link to="/courses">Courses</Link> |{" "}
            <Link to="/prerequisites">Prerequisites</Link> |{" "}
            <Link to="/classrooms">Classrooms</Link> |{" "}
            <Link to="/schedules">Schedules</Link> |{" "}
            <Link to="/enrollments">Enrollments</Link> |{" "}
            <Link to="/grades">Grades</Link> |{" "}
            <Link to="/assignments">Assignments</Link> |{" "}
            <button onClick={handleLogout}>Logout</button>
          </>
        ) : (
          <Link to="/login">Login</Link>
        )}
      </nav>
      <hr />
      <Routes>
        <Route path="/login" element={<LoginPage onLogin={handleLogin} />} />
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
        <Route path="/prerequisites" element={<PrerequisiteListPage />} />
        <Route path="/prerequisites/new" element={<PrerequisiteFormPage />} />
        <Route path="/prerequisites/:id/edit" element={<PrerequisiteFormPage />} />
        <Route path="/classrooms" element={<ClassroomListPage />} />
        <Route path="/classrooms/new" element={<ClassroomFormPage />} />
        <Route path="/classrooms/:id/edit" element={<ClassroomFormPage />} />
        <Route path="/schedules" element={<ScheduleListPage />} />
        <Route path="/schedules/new" element={<ScheduleFormPage />} />
        <Route path="/schedules/:id/edit" element={<ScheduleFormPage />} />
        <Route path="/enrollments" element={<EnrollmentListPage />} />
        <Route path="/enrollments/new" element={<EnrollmentFormPage />} />
        <Route path="/grades" element={<GradeListPage />} />
        <Route path="/grades/new" element={<GradeFormPage />} />
        <Route path="/assignments" element={<AssignmentListPage />} />
        <Route path="/assignments/new" element={<AssignmentFormPage />} />
        <Route path="/assignments/:id/edit" element={<AssignmentFormPage />} />
      </Routes>
    </div>
  );
}

export default function Root() {
  return (
    <BrowserRouter>
      <App />
    </BrowserRouter>
  );
}