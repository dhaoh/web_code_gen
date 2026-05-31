import React from 'react';
import { Outlet, Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../AuthContext';

export default function Layout() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  if (!user) return <div>Loading...</div>;

  return (
    <div className="container-fluid">
      <nav className="navbar navbar-expand-lg navbar-light bg-light mb-4">
        <div className="container-fluid">
          <Link className="navbar-brand" to="/">Course System</Link>
          <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
            <span className="navbar-toggler-icon" />
          </button>
          <div className="collapse navbar-collapse" id="navbarNav">
            <ul className="navbar-nav me-auto">
              {user.role === 'admin' && (
                <>
                  <li className="nav-item"><Link className="nav-link" to="/users">Users</Link></li>
                  <li className="nav-item"><Link className="nav-link" to="/departments">Departments</Link></li>
                  <li className="nav-item"><Link className="nav-link" to="/courses">Courses</Link></li>
                  <li className="nav-item"><Link className="nav-link" to="/enrollments">Enrollments</Link></li>
                </>
              )}
              {user.role === 'teacher' && (
                <>
                  <li className="nav-item"><Link className="nav-link" to="/courses">My Courses</Link></li>
                  <li className="nav-item"><Link className="nav-link" to="/enrollments">Enrollments</Link></li>
                  <li className="nav-item"><Link className="nav-link" to="/grades">Grades</Link></li>
                  <li className="nav-item"><Link className="nav-link" to="/assignments">Assignments</Link></li>
                  <li className="nav-item"><Link className="nav-link" to="/submissions">Submissions</Link></li>
                </>
              )}
              {user.role === 'student' && (
                <>
                  <li className="nav-item"><Link className="nav-link" to="/available-courses">Available Courses</Link></li>
                  <li className="nav-item"><Link className="nav-link" to="/my-enrollments">My Enrollments</Link></li>
                  <li className="nav-item"><Link className="nav-link" to="/my-grades">My Grades</Link></li>
                  <li className="nav-item"><Link className="nav-link" to="/assignments">Assignments</Link></li>
                  <li className="nav-item"><Link className="nav-link" to="/submissions">Submissions</Link></li>
                </>
              )}
            </ul>
            <span className="navbar-text me-3">
              {user.full_name} ({user.role})
            </span>
            <button className="btn btn-outline-danger" onClick={handleLogout}>Logout</button>
          </div>
        </div>
      </nav>
      <div className="container">
        <Outlet />
      </div>
    </div>
  );
}