import { BrowserRouter, Routes, Route, NavLink } from 'react-router-dom';
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

const API_BASE = 'http://localhost:8000';

function App() {
    return (
        <BrowserRouter>
            <div className="flex h-screen overflow-hidden">
                {/* Sidebar */}
                <aside className="w-64 bg-slate-900 text-white flex flex-col shrink-0">
                    <div className="p-5 border-b border-slate-700">
                        <h1 className="text-lg font-bold tracking-tight">
                            ⚙️ Student Course System Medium
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
                            to="/users"
                            className={({ isActive }) =>
                                `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition ${
                                    isActive ? 'bg-indigo-600 text-white' : 'text-slate-300 hover:bg-slate-800 hover:text-white'
                                }`
                            }
                        >
                            <span className="text-base">User</span>
                        </NavLink>
                        <NavLink
                            to="/departments"
                            className={({ isActive }) =>
                                `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition ${
                                    isActive ? 'bg-indigo-600 text-white' : 'text-slate-300 hover:bg-slate-800 hover:text-white'
                                }`
                            }
                        >
                            <span className="text-base">Department</span>
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
                        <NavLink
                            to="/grades"
                            className={({ isActive }) =>
                                `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition ${
                                    isActive ? 'bg-indigo-600 text-white' : 'text-slate-300 hover:bg-slate-800 hover:text-white'
                                }`
                            }
                        >
                            <span className="text-base">Grade</span>
                        </NavLink>
                        <NavLink
                            to="/assignments"
                            className={({ isActive }) =>
                                `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition ${
                                    isActive ? 'bg-indigo-600 text-white' : 'text-slate-300 hover:bg-slate-800 hover:text-white'
                                }`
                            }
                        >
                            <span className="text-base">Assignment</span>
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
                        <Route path="/users" element={<UserListPage apiBaseUrl={API_BASE} />} />
                        <Route path="/users/new" element={<UserFormPage />} />
                        <Route path="/users/:id/edit" element={<UserFormPage />} />
                        <Route path="/departments" element={<DepartmentListPage apiBaseUrl={API_BASE} />} />
                        <Route path="/departments/new" element={<DepartmentFormPage />} />
                        <Route path="/departments/:id/edit" element={<DepartmentFormPage />} />
                        <Route path="/courses" element={<CourseListPage apiBaseUrl={API_BASE} />} />
                        <Route path="/courses/new" element={<CourseFormPage />} />
                        <Route path="/courses/:id/edit" element={<CourseFormPage />} />
                        <Route path="/enrollments" element={<EnrollmentListPage apiBaseUrl={API_BASE} />} />
                        <Route path="/enrollments/new" element={<EnrollmentFormPage />} />
                        <Route path="/enrollments/:id/edit" element={<EnrollmentFormPage />} />
                        <Route path="/grades" element={<GradeListPage apiBaseUrl={API_BASE} />} />
                        <Route path="/grades/new" element={<GradeFormPage />} />
                        <Route path="/grades/:id/edit" element={<GradeFormPage />} />
                        <Route path="/assignments" element={<AssignmentListPage apiBaseUrl={API_BASE} />} />
                        <Route path="/assignments/new" element={<AssignmentFormPage />} />
                        <Route path="/assignments/:id/edit" element={<AssignmentFormPage />} />
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
                <p className="text-slate-500 mt-1">A complete student course selection and management system with users, departments, courses, enrollments, and grades. Teachers manage courses,...</p>
            </div>

            {/* Stats */}
            <div className="grid grid-cols-3 gap-5 mb-8">
                <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-5 hover:shadow-md transition">
                    <div className="flex items-center justify-between mb-3">
                        <span className="text-2xl">User</span>
                        <span className="text-3xl">
👥                        </span>
                    </div>
                    <p className="text-xs text-slate-400 mb-3">
                        6 attributes                    </p>
                    <a
                        href="/users"
                        className="inline-flex items-center gap-1 text-sm font-medium text-indigo-600 hover:text-indigo-800 transition"
                    >
                        Manage <span className="text-xs">→</span>
                    </a>
                </div>
                <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-5 hover:shadow-md transition">
                    <div className="flex items-center justify-between mb-3">
                        <span className="text-2xl">Department</span>
                        <span className="text-3xl">
🏛️                        </span>
                    </div>
                    <p className="text-xs text-slate-400 mb-3">
                        3 attributes&middot; 1 relation                    </p>
                    <a
                        href="/departments"
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
                        6 attributes&middot; 3 relations                    </p>
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
                <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-5 hover:shadow-md transition">
                    <div className="flex items-center justify-between mb-3">
                        <span className="text-2xl">Grade</span>
                        <span className="text-3xl">
📊                        </span>
                    </div>
                    <p className="text-xs text-slate-400 mb-3">
                        5 attributes                    </p>
                    <a
                        href="/grades"
                        className="inline-flex items-center gap-1 text-sm font-medium text-indigo-600 hover:text-indigo-800 transition"
                    >
                        Manage <span className="text-xs">→</span>
                    </a>
                </div>
                <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-5 hover:shadow-md transition">
                    <div className="flex items-center justify-between mb-3">
                        <span className="text-2xl">Assignment</span>
                        <span className="text-3xl">
📝                        </span>
                    </div>
                    <p className="text-xs text-slate-400 mb-3">
                        6 attributes&middot; 1 relation                    </p>
                    <a
                        href="/assignments"
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
                            <p className="text-xs text-slate-500 mt-0.5">Prevent enrollment when the course has reached its maximum capacity.
</p>
                        </div>
                    </div>
                    <div className="flex items-start gap-3 p-3 bg-slate-50 rounded-lg">
                        <span className={`mt-0.5 w-2 h-2 rounded-full shrink-0 bg-red-500`}></span>
                        <div>
                            <span className="text-sm font-semibold text-slate-800">Duplicate Enrollment</span>
                            <span className={`ml-2 text-[10px] px-1.5 py-0.5 rounded-full font-medium uppercase bg-red-100 text-red-700`}>critical</span>
                            <p className="text-xs text-slate-500 mt-0.5">Prevent a student from enrolling in the same course more than once.
</p>
                        </div>
                    </div>
                    <div className="flex items-start gap-3 p-3 bg-slate-50 rounded-lg">
                        <span className={`mt-0.5 w-2 h-2 rounded-full shrink-0 bg-red-500`}></span>
                        <div>
                            <span className="text-sm font-semibold text-slate-800">Student Role Check</span>
                            <span className={`ml-2 text-[10px] px-1.5 py-0.5 rounded-full font-medium uppercase bg-red-100 text-red-700`}>critical</span>
                            <p className="text-xs text-slate-500 mt-0.5">Only users with role 'student' can enroll in courses. Only users with role 'teacher' can be assigned as course instructors.
</p>
                        </div>
                    </div>
                    <div className="flex items-start gap-3 p-3 bg-slate-50 rounded-lg">
                        <span className={`mt-0.5 w-2 h-2 rounded-full shrink-0 bg-amber-500`}></span>
                        <div>
                            <span className="text-sm font-semibold text-slate-800">Grade Assignment</span>
                            <span className={`ml-2 text-[10px] px-1.5 py-0.5 rounded-full font-medium uppercase bg-amber-100 text-amber-700`}>important</span>
                            <p className="text-xs text-slate-500 mt-0.5">A grade can only be assigned to an existing enrollment. One enrollment can have at most one grade.
</p>
                        </div>
                    </div>
                    <div className="flex items-start gap-3 p-3 bg-slate-50 rounded-lg">
                        <span className={`mt-0.5 w-2 h-2 rounded-full shrink-0 bg-amber-500`}></span>
                        <div>
                            <span className="text-sm font-semibold text-slate-800">Credit Limit</span>
                            <span className={`ml-2 text-[10px] px-1.5 py-0.5 rounded-full font-medium uppercase bg-amber-100 text-amber-700`}>important</span>
                            <p className="text-xs text-slate-500 mt-0.5">A student cannot enroll in courses totaling more than 30 credits per semester.
</p>
                        </div>
                    </div>
                    <div className="flex items-start gap-3 p-3 bg-slate-50 rounded-lg">
                        <span className={`mt-0.5 w-2 h-2 rounded-full shrink-0 bg-blue-400`}></span>
                        <div>
                            <span className="text-sm font-semibold text-slate-800">Assignment Deadline</span>
                            <span className={`ml-2 text-[10px] px-1.5 py-0.5 rounded-full font-medium uppercase bg-blue-100 text-blue-700`}>nice_to_have</span>
                            <p className="text-xs text-slate-500 mt-0.5">Assignments submitted after the due date should be marked as late.
</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default App;
