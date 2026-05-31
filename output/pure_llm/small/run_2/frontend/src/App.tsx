import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import StudentListPage from './pages/StudentListPage';
import StudentFormPage from './pages/StudentFormPage';
import CourseListPage from './pages/CourseListPage';
import CourseFormPage from './pages/CourseFormPage';
import EnrollmentPage from './pages/EnrollmentPage';

function App() {
  return (
    <BrowserRouter>
      <div>
        <nav style={{ padding: '1rem', borderBottom: '1px solid #ccc', marginBottom: '1rem' }}>
          <Link to="/students" style={{ marginRight: '1rem' }}>Students</Link>
          <Link to="/courses" style={{ marginRight: '1rem' }}>Courses</Link>
          <Link to="/enrollments">Enrollments</Link>
        </nav>
        <Routes>
          <Route path="/" element={<StudentListPage />} />
          <Route path="/students" element={<StudentListPage />} />
          <Route path="/students/new" element={<StudentFormPage />} />
          <Route path="/students/edit/:id" element={<StudentFormPage />} />
          <Route path="/courses" element={<CourseListPage />} />
          <Route path="/courses/new" element={<CourseFormPage />} />
          <Route path="/courses/edit/:id" element={<CourseFormPage />} />
          <Route path="/enrollments" element={<EnrollmentPage />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;