import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import UserList from "./pages/UserListPage";
import UserForm from "./pages/UserFormPage";
import DepartmentList from "./pages/DepartmentListPage";
import DepartmentForm from "./pages/DepartmentFormPage";
import CourseList from "./pages/CourseListPage";
import CourseForm from "./pages/CourseFormPage";
import EnrollmentList from "./pages/EnrollmentListPage";
import EnrollmentForm from "./pages/EnrollmentFormPage";
import GradeList from "./pages/GradeListPage";
import GradeForm from "./pages/GradeFormPage";
import AssignmentList from "./pages/AssignmentListPage";
import AssignmentForm from "./pages/AssignmentFormPage";

const App: React.FC = () => {
  return (
    <Router>
      <div style={{ padding: "1rem" }}>
        <nav>
          <Link to="/users">Users</Link> | <Link to="/departments">Departments</Link> |{" "}
          <Link to="/courses">Courses</Link> | <Link to="/enrollments">Enrollments</Link> |{" "}
          <Link to="/grades">Grades</Link> | <Link to="/assignments">Assignments</Link>
        </nav>
        <hr />
        <Routes>
          <Route path="/users" element={<UserList />} />
          <Route path="/users/new" element={<UserForm />} />
          <Route path="/users/:id/edit" element={<UserForm />} />
          <Route path="/departments" element={<DepartmentList />} />
          <Route path="/departments/new" element={<DepartmentForm />} />
          <Route path="/departments/:id/edit" element={<DepartmentForm />} />
          <Route path="/courses" element={<CourseList />} />
          <Route path="/courses/new" element={<CourseForm />} />
          <Route path="/courses/:id/edit" element={<CourseForm />} />
          <Route path="/enrollments" element={<EnrollmentList />} />
          <Route path="/enrollments/new" element={<EnrollmentForm />} />
          <Route path="/enrollments/:id/edit" element={<EnrollmentForm />} />
          <Route path="/grades" element={<GradeList />} />
          <Route path="/grades/new" element={<GradeForm />} />
          <Route path="/grades/:id/edit" element={<GradeForm />} />
          <Route path="/assignments" element={<AssignmentList />} />
          <Route path="/assignments/new" element={<AssignmentForm />} />
          <Route path="/assignments/:id/edit" element={<AssignmentForm />} />
          <Route path="/" element={<h2>Welcome to Student Course System</h2>} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;