import React from "react";
import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import StudentListPage from "./pages/StudentListPage";
import StudentFormPage from "./pages/StudentFormPage";
import CourseListPage from "./pages/CourseListPage";
import CourseFormPage from "./pages/CourseFormPage";
import EnrollmentListPage from "./pages/EnrollmentListPage";
import EnrollmentFormPage from "./pages/EnrollmentFormPage";

function App() {
  return (
    <BrowserRouter>
      <div className="container mx-auto p-4">
        <nav className="mb-6 flex gap-4 bg-gray-100 p-3 rounded">
          <Link to="/students" className="text-blue-600 underline">Students</Link>
          <Link to="/courses" className="text-blue-600 underline">Courses</Link>
          <Link to="/enrollments" className="text-blue-600 underline">Enrollments</Link>
        </nav>
        <Routes>
          <Route path="/" element={<StudentListPage />} />
          <Route path="/students" element={<StudentListPage />} />
          <Route path="/students/new" element={<StudentFormPage />} />
          <Route path="/students/:id/edit" element={<StudentFormPage />} />
          <Route path="/courses" element={<CourseListPage />} />
          <Route path="/courses/new" element={<CourseFormPage />} />
          <Route path="/courses/:id/edit" element={<CourseFormPage />} />
          <Route path="/enrollments" element={<EnrollmentListPage />} />
          <Route path="/enrollments/new" element={<EnrollmentFormPage />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;