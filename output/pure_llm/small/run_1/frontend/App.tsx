import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import StudentsListPage from "./pages/StudentsListPage";
import StudentFormPage from "./pages/StudentFormPage";
import CoursesListPage from "./pages/CoursesListPage";
import CourseFormPage from "./pages/CourseFormPage";
import EnrollmentsListPage from "./pages/EnrollmentsListPage";
import EnrollmentFormPage from "./pages/EnrollmentFormPage";

const App: React.FC = () => {
  return (
    <Router>
      <div>
        <nav>
          <ul style={{ display: "flex", listStyle: "none", gap: "1rem" }}>
            <li><Link to="/students">Students</Link></li>
            <li><Link to="/courses">Courses</Link></li>
            <li><Link to="/enrollments">Enrollments</Link></li>
          </ul>
        </nav>
        <hr />
        <Routes>
          <Route path="/" element={<h1>Welcome to Student Course System</h1>} />
          <Route path="/students" element={<StudentsListPage />} />
          <Route path="/students/new" element={<StudentFormPage />} />
          <Route path="/students/:id/edit" element={<StudentFormPage />} />
          <Route path="/courses" element={<CoursesListPage />} />
          <Route path="/courses/new" element={<CourseFormPage />} />
          <Route path="/courses/:id/edit" element={<CourseFormPage />} />
          <Route path="/enrollments" element={<EnrollmentsListPage />} />
          <Route path="/enrollments/new" element={<EnrollmentFormPage />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;