import { ReactNode } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { User } from '../api'

interface Props {
  user: User
  onLogout: () => void
  children: ReactNode
}

export default function Layout({ user, onLogout, children }: Props) {
  const navigate = useNavigate()
  const handleLogout = () => {
    onLogout()
    navigate('/')
  }

  return (
    <div style={{ display: 'flex' }}>
      <nav style={{ width: 200, padding: 16, borderRight: '1px solid #ccc' }}>
        <h3>{user.full_name} ({user.role})</h3>
        {user.role === 'admin' && (
          <>
            <div><Link to="/users">Users</Link></div>
            <div><Link to="/departments">Departments</Link></div>
            <div><Link to="/courses">Courses</Link></div>
            <div><Link to="/enrollments">Enrollments</Link></div>
            <div><Link to="/grades">Grades</Link></div>
            <div><Link to="/assignments">Assignments</Link></div>
          </>
        )}
        {user.role === 'teacher' && (
          <>
            <div><Link to="/teacher/courses">My Courses</Link></div>
          </>
        )}
        {user.role === 'student' && (
          <>
            <div><Link to="/student/enrollments">My Enrollments</Link></div>
            <div><Link to="/student/enroll">Enroll in Course</Link></div>
          </>
        )}
        <button onClick={handleLogout} style={{ marginTop: 16 }}>Logout</button>
      </nav>
      <main style={{ flex: 1, padding: 16 }}>
        {children}
      </main>
    </div>
  )
}