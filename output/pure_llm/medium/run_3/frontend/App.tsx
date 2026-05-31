import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Link, Navigate } from 'react-router-dom';
import { api, setToken } from './api';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import Dashboard from './pages/Dashboard';
import UsersListPage from './pages/UsersListPage';
import UserFormPage from './pages/UserFormPage';
import DepartmentsListPage from './pages/DepartmentsListPage';
import DepartmentFormPage from './pages/DepartmentFormPage';
import CoursesListPage from './pages/CoursesListPage';
import CourseFormPage from './pages/CourseFormPage';
import EnrollmentsListPage from './pages/EnrollmentsListPage';
import EnrollmentFormPage from './pages/EnrollmentFormPage';
import GradesListPage from './pages/GradesListPage';
import GradeFormPage from './pages/GradeFormPage';
import AssignmentsListPage from './pages/AssignmentsListPage';
import AssignmentFormPage from './pages/AssignmentFormPage';

interface User {
  id: number;
  username: string;
  role: string;
  full_name: string;
  email: string;
}

const AuthContext = React.createContext<{
  user: User | null;
  login: (token: string) => void;
  logout: () => void;
}>({
  user: null,
  login: () => {},
  logout: () => {},
});

export const useAuth = () => React.useContext(AuthContext);

function App() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  const login = async (token: string) => {
    setToken(token);
    try {
      const me = await api.getMe();
      setUser(me);
    } catch {
      setToken(null);
    }
  };

  const logout = () => {
    setToken(null);
    setUser(null);
  };

  useEffect(() => {
    const init = async () => {
      const t = localStorage.getItem('token');
      if (t) {
        setToken(t);
        try {
          const me = await api.getMe();
          setUser(me);
        } catch {
          setToken(null);
        }
      }
      setLoading(false);
    };
    init();
  }, []);

  if (loading) return <div>Loading...</div>;

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      <BrowserRouter>
        <nav style={{ padding: '8px', background: '#f0f0f0', marginBottom: 16 }}>
          <Link to="/">Home</Link>
          {user ? (
            <>
              <Link to="/dashboard" style={{ marginLeft: 16 }}>Dashboard</Link>
              <button onClick={logout} style={{ marginLeft: 16 }}>Logout ({user.username})</button>
            </>
          ) : (
            <>
              <Link to="/login" style={{ marginLeft: 16 }}>Login</Link>
              <Link to="/register" style={{ marginLeft: 16 }}>Register</Link>
            </>
          )}
        </nav>

        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/dashboard" element={user ? <Dashboard /> : <Navigate to="/login" />} />
          
          {/* User routes */}
          <Route path="/users" element={user ? <UsersListPage /> : <Navigate to="/login" />} />
          <Route path="/users/new" element={user ? <UserFormPage /> : <Navigate to="/login" />} />
          <Route path="/users/:id/edit" element={user ? <UserFormPage /> : <Navigate to="/login" />} />
          
          {/* Department routes */}
          <Route path="/departments" element={user ? <DepartmentsListPage /> : <Navigate to="/login" />} />
          <Route path="/departments/new" element={user ? <DepartmentFormPage /> : <Navigate to="/login" />} />
          <Route path="/departments/:id/edit" element={user ? <DepartmentFormPage /> : <Navigate to="/login" />} />
          
          {/* Course routes */}
          <Route path="/courses" element={user ? <CoursesListPage /> : <Navigate to="/login" />} />
          <Route path="/courses/new" element={user ? <CourseFormPage /> : <Navigate to="/login" />} />
          <Route path="/courses/:id/edit" element={user ? <CourseFormPage /> : <Navigate to="/login" />} />
          
          {/* Enrollment routes */}
          <Route path="/enrollments" element={user ? <EnrollmentsListPage /> : <Navigate to="/login" />} />
          <Route path="/enrollments/new" element={user ? <EnrollmentFormPage /> : <Navigate to="/login" />} />
          
          {/* Grade routes */}
          <Route path="/grades" element={user ? <GradesListPage /> : <Navigate to="/login" />} />
          <Route path="/grades/new" element={user ? <GradeFormPage /> : <Navigate to="/login" />} />
          <Route path="/grades/:id/edit" element={user ? <GradeFormPage /> : <Navigate to="/login" />} />
          
          {/* Assignment routes */}
          <Route path="/assignments" element={user ? <AssignmentsListPage /> : <Navigate to="/login" />} />
          <Route path="/assignments/new" element={user ? <AssignmentFormPage /> : <Navigate to="/login" />} />
          <Route path="/assignments/:id/edit" element={user ? <AssignmentFormPage /> : <Navigate to="/login" />} />
          
          <Route path="*" element={<div>404 Not Found</div>} />
        </Routes>
      </BrowserRouter>
    </AuthContext.Provider>
  );
}

function Home() {
  return <div><h1>Student Course System</h1><p>Welcome to the student course management system.</p></div>;
}

export default App;