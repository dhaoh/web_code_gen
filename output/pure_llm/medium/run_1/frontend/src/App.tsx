import { useState, useEffect } from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import { User } from './api'
import Login from './pages/Login'
import Layout from './components/Layout'
import UserList from './pages/UserList'
import UserForm from './pages/UserForm'
import DepartmentList from './pages/DepartmentList'
import DepartmentForm from './pages/DepartmentForm'
import CourseList from './pages/CourseList'
import CourseForm from './pages/CourseForm'
import EnrollmentList from './pages/EnrollmentList'
import EnrollmentForm from './pages/EnrollmentForm'
import GradeList from './pages/GradeList'
import GradeForm from './pages/GradeForm'
import AssignmentList from './pages/AssignmentList'
import AssignmentForm from './pages/AssignmentForm'
import StudentEnrollments from './pages/StudentEnrollments'
import StudentEnroll from './pages/StudentEnroll'
import TeacherCourses from './pages/TeacherCourses'
import CourseEnrollments from './pages/CourseEnrollments'

function App() {
  const [user, setUser] = useState<User | null>(null)

  useEffect(() => {
    const stored = localStorage.getItem('user')
    if (stored) {
      setUser(JSON.parse(stored))
    }
  }, [])

  const handleLogin = (u: User) => {
    localStorage.setItem('user', JSON.stringify(u))
    setUser(u)
  }

  const handleLogout = () => {
    localStorage.removeItem('user')
    setUser(null)
  }

  if (!user) {
    return <Login onLogin={handleLogin} />
  }

  return (
    <Layout user={user} onLogout={handleLogout}>
      <Routes>
        {/* Admin full CRUD */}
        {user.role === 'admin' && (
          <>
            <Route path="/users" element={<UserList />} />
            <Route path="/users/new" element={<UserForm />} />
            <Route path="/users/:id/edit" element={<UserForm />} />
            <Route path="/departments" element={<DepartmentList />} />
            <Route path="/departments/new" element={<DepartmentForm />} />
            <Route path="/departments/:id/edit" element={<DepartmentForm />} />
            <Route path="/courses" element={<CourseList />} />
            <Route path="/courses/new" element={<CourseForm />} />
            <Route path="/courses/:id/edit" element={<CourseForm />} />
            <Route path="/enrollments" element={<EnrollmentList />} />
            <Route path="/enrollments/new" element={<EnrollmentForm />} />
            <Route path="/grades" element={<GradeList />} />
            <Route path="/grades/new" element={<GradeForm />} />
            <Route path="/assignments" element={<AssignmentList />} />
            <Route path="/assignments/new" element={<AssignmentForm />} />
            <Route path="/" element={<Navigate to="/users" />} />
          </>
        )}

        {/* Teacher */}
        {user.role === 'teacher' && (
          <>
            <Route path="/teacher/courses" element={<TeacherCourses />} />
            <Route path="/teacher/courses/:courseId/enrollments" element={<CourseEnrollments />} />
            <Route path="/teacher/courses/:courseId/assignments" element={<AssignmentList />} />
            <Route path="/teacher/courses/:courseId/assignments/new" element={<AssignmentForm />} />
            <Route path="/teacher/courses/:courseId/assignments/:assignmentId/edit" element={<AssignmentForm />} />
            <Route path="/" element={<Navigate to="/teacher/courses" />} />
          </>
        )}

        {/* Student */}
        {user.role === 'student' && (
          <>
            <Route path="/student/enrollments" element={<StudentEnrollments />} />
            <Route path="/student/enroll" element={<StudentEnroll />} />
            <Route path="/" element={<Navigate to="/student/enrollments" />} />
          </>
        )}
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </Layout>
  )
}

export default App