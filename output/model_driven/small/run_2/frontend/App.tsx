import { BrowserRouter, Routes, Route, NavLink } from 'react-router-dom';
import StudentListPage from './pages/StudentListPage';
import StudentFormPage from './pages/StudentFormPage';
import CourseListPage from './pages/CourseListPage';
import CourseFormPage from './pages/CourseFormPage';
import EnrollmentListPage from './pages/EnrollmentListPage';
import EnrollmentFormPage from './pages/EnrollmentFormPage';

const API_BASE = 'http://localhost:8000';

function App() {
    return (
        <BrowserRouter>
            <div className="flex h-screen overflow-hidden">
                {/* Sidebar */}
                <aside className="w-64 bg-slate-900 text-white flex flex-col shrink-0">
                    <div className="p-5 border-b border-slate-700">
                        <h1 className="text-lg font-bold tracking-tight">
                            ⚙️ Student Course System Small
                        </h1>
                    </div>
                    <nav className="flex-1 overflow-y-auto p-3 space-y-1">
                        <NavLink
                            to="/"
                            end
                            className={({ isActive }) =>
                                `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition ${
                                    isActive ? 'bg-indigo-600 text-white' : 'text-slate-300 hover:bg-slate-800 hover:text-white'
                                }`
                            }
                        >
                            <span className="text-base">🏠</span> Dashboard
                        </NavLink>
                        <NavLink
                            to="/students"
                            className={({ isActive }) =>
                                `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition ${
                                    isActive ? 'bg-indigo-600 text-white' : 'text-slate-300 hover:bg-slate-800 hover:text-white'
                                }`
                            }
                        >
                            <span className="text-base">Student</span>
                        </NavLink>
                        <NavLink
                            to="/courses"
                            className={({ isActive }) =>
                                `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition ${
                                    isActive ? 'bg-indigo-600 text-white' : 'text-slate-300 hover:bg-slate-800 hover:text-white'
                                }`
                            }
                        >
                            <span className="text-base">Course</span>
                        </NavLink>
                        <NavLink
                            to="/enrollments"
                            className={({ isActive }) =>
                                `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition ${
                                    isActive ? 'bg-indigo-600 text-white' : 'text-slate-300 hover:bg-slate-800 hover:text-white'
                                }`
                            }
                        >
                            <span className="text-base">Enrollment</span>
                        </NavLink>
                    </nav>
                    <div className="p-4 border-t border-slate-700 text-xs text-slate-500">
                        Generated via Model-Driven Approach
                    </div>
                </aside>

                {/* Main content */}
                <main className="flex-1 overflow-y-auto bg-slate-100">
                    <Routes>
                        <Route path="/" element={<Dashboard />} />
                        <Route path="/students" element={<StudentListPage apiBaseUrl={API_BASE} />} />
                        <Route path="/students/new" element={<StudentFormPage />} />
                        <Route path="/students/:id/edit" element={<StudentFormPage />} />
                        <Route path="/courses" element={<CourseListPage apiBaseUrl={API_BASE} />} />
                        <Route path="/courses/new" element={<CourseFormPage />} />
                        <Route path="/courses/:id/edit" element={<CourseFormPage />} />
                        <Route path="/enrollments" element={<EnrollmentListPage apiBaseUrl={API_BASE} />} />
                        <Route path="/enrollments/new" element={<EnrollmentFormPage />} />
                        <Route path="/enrollments/:id/edit" element={<EnrollmentFormPage />} />
                    </Routes>
                </main>
            </div>
        </BrowserRouter>
    );
}

function Dashboard() {
    return (
        <div className="p-8">
            <div className="mb-8">
                <h1 className="text-3xl font-bold text-slate-900">Dashboard</h1>
                <p className="text-slate-500 mt-1">A simple student course selection system. Students can browse available courses and enroll. The system tracks enrollments and prevents...</p>
            </div>

            {/* Stats */}
            <div className="grid grid-cols-3 gap-5 mb-8">
                <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-5 hover:shadow-md transition">
                    <div className="flex items-center justify-between mb-3">
                        <span className="text-2xl">Student</span>
                        <span className="text-3xl">
👤                        </span>
                    </div>
                    <p className="text-xs text-slate-400 mb-3">
                        3 attributes&middot; 1 relation                    </p>
                    <a
                        href="/students"
                        className="inline-flex items-center gap-1 text-sm font-medium text-indigo-600 hover:text-indigo-800 transition"
                    >
                        Manage <span className="text-xs">→</span>
                    </a>
                </div>
                <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-5 hover:shadow-md transition">
                    <div className="flex items-center justify-between mb-3">
                        <span className="text-2xl">Course</span>
                        <span className="text-3xl">
📚                        </span>
                    </div>
                    <p className="text-xs text-slate-400 mb-3">
                        4 attributes&middot; 1 relation                    </p>
                    <a
                        href="/courses"
                        className="inline-flex items-center gap-1 text-sm font-medium text-indigo-600 hover:text-indigo-800 transition"
                    >
                        Manage <span className="text-xs">→</span>
                    </a>
                </div>
                <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-5 hover:shadow-md transition">
                    <div className="flex items-center justify-between mb-3">
                        <span className="text-2xl">Enrollment</span>
                        <span className="text-3xl">
📋                        </span>
                    </div>
                    <p className="text-xs text-slate-400 mb-3">
                        4 attributes                    </p>
                    <a
                        href="/enrollments"
                        className="inline-flex items-center gap-1 text-sm font-medium text-indigo-600 hover:text-indigo-800 transition"
                    >
                        Manage <span className="text-xs">→</span>
                    </a>
                </div>
            </div>

            {/* Business Rules */}
            <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
                <h2 className="text-lg font-semibold text-slate-900 mb-4">🏷️ Business Rules</h2>
                <div className="space-y-3">
                    <div className="flex items-start gap-3 p-3 bg-slate-50 rounded-lg">
                        <span className={`mt-0.5 w-2 h-2 rounded-full shrink-0 bg-red-500`}></span>
                        <div>
                            <span className="text-sm font-semibold text-slate-800">Capacity Check</span>
                            <span className={`ml-2 text-[10px] px-1.5 py-0.5 rounded-full font-medium uppercase bg-red-100 text-red-700`}>critical</span>
                            <p className="text-xs text-slate-500 mt-0.5">Prevent enrollment when the course has reached its maximum capacity. The system must count current enrollments and compare against course.capacity before allowing a new enrollment.
</p>
                        </div>
                    </div>
                    <div className="flex items-start gap-3 p-3 bg-slate-50 rounded-lg">
                        <span className={`mt-0.5 w-2 h-2 rounded-full shrink-0 bg-red-500`}></span>
                        <div>
                            <span className="text-sm font-semibold text-slate-800">Duplicate Enrollment</span>
                            <span className={`ml-2 text-[10px] px-1.5 py-0.5 rounded-full font-medium uppercase bg-red-100 text-red-700`}>critical</span>
                            <p className="text-xs text-slate-500 mt-0.5">Prevent a student from enrolling in the same course more than once. The system must check for existing enrollment with the same student_id and course_id before creating a new one.
</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default App;
