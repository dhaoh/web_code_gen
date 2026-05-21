import React from 'react';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import StudentListPage from './pages/StudentListPage';
import StudentFormPage from './pages/StudentFormPage';
import CourseListPage from './pages/CourseListPage';
import CourseFormPage from './pages/CourseFormPage';
import EnrollmentListPage from './pages/EnrollmentListPage';
import EnrollmentFormPage from './pages/EnrollmentFormPage';

function App() {
    return (
        <BrowserRouter>
            <div className="min-h-screen bg-gray-50">
                <nav className="bg-white shadow-sm border-b">
                    <div className="max-w-6xl mx-auto flex gap-6 p-4">
                        <Link to="/" className="font-bold text-lg">
                            Student Course System Small
                        </Link>
                        <Link to="/students" className="text-gray-600 hover:text-gray-900">
                            Student
                        </Link>
                        <Link to="/courses" className="text-gray-600 hover:text-gray-900">
                            Course
                        </Link>
                        <Link to="/enrollments" className="text-gray-600 hover:text-gray-900">
                            Enrollment
                        </Link>
                    </div>
                </nav>
                <main className="max-w-6xl mx-auto">
                    <Routes>
                        <Route path="/" element={<HomePage />} />
                        <Route path="/students" element={<StudentListPage />} />
                        <Route path="/students/new" element={<StudentFormPage />} />
                        <Route path="/students/:id/edit" element={<StudentFormPage />} />
                        <Route path="/courses" element={<CourseListPage />} />
                        <Route path="/courses/new" element={<CourseFormPage />} />
                        <Route path="/courses/:id/edit" element={<CourseFormPage />} />
                        <Route path="/enrollments" element={<EnrollmentListPage />} />
                        <Route path="/enrollments/new" element={<EnrollmentFormPage />} />
                        <Route path="/enrollments/:id/edit" element={<EnrollmentFormPage />} />
                    </Routes>
                </main>
            </div>
        </BrowserRouter>
    );
}

function HomePage() {
    return (
        <div className="p-8">
            <h1 className="text-3xl font-bold mb-4">Student Course System Small</h1>
            <p className="text-gray-600 mb-6">A simple student course selection system. Students can browse available courses and enroll. The system tracks enrollments and prevents over-capacity enrollment.
</p>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                <Link
                    to="/students"
                    className="block p-4 bg-white rounded-lg shadow hover:shadow-md transition"
                >
                    <h2 className="text-xl font-semibold">Students</h2>
                    <p className="text-gray-500 text-sm mt-1">
                        3 fields
                        (ID: id)
                    </p>
                </Link>
                <Link
                    to="/courses"
                    className="block p-4 bg-white rounded-lg shadow hover:shadow-md transition"
                >
                    <h2 className="text-xl font-semibold">Courses</h2>
                    <p className="text-gray-500 text-sm mt-1">
                        4 fields
                        (ID: id)
                    </p>
                </Link>
                <Link
                    to="/enrollments"
                    className="block p-4 bg-white rounded-lg shadow hover:shadow-md transition"
                >
                    <h2 className="text-xl font-semibold">Enrollments</h2>
                    <p className="text-gray-500 text-sm mt-1">
                        4 fields
                        (ID: id)
                    </p>
                </Link>
            </div>
        </div>
    );
}

export default App;
