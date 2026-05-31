import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../App';

const Dashboard: React.FC = () => {
  const { user } = useAuth();
  if (!user) return null;

  return (
    <div>
      <h2>Dashboard</h2>
      <p>Welcome, {user.full_name} ({user.role})</p>
      <ul>
        {user.role === 'teacher' && (
          <>
            <li><Link to="/users">Manage Users</Link></li>
            <li><Link to="/departments">Manage Departments</Link></li>
            <li><Link to="/courses">Manage Courses</Link></li>
            <li><Link to="/enrollments">View Enrollments</Link></li>
            <li><Link to="/grades">Manage Grades</Link></li>
            <li><Link to="/assignments">Manage Assignments</Link></li>
          </>
        )}
        {user.role === 'student' && (
          <>
            <li><Link to="/courses">Browse Courses</Link></li>
            <li><Link to="/enrollments">My Enrollments</Link></li>
            <li><Link to="/grades">My Grades</Link></li>
            <li><Link to="/assignments">Assignments</Link></li>
          </>
        )}
      </ul>
    </div>
  );
};

export default Dashboard;