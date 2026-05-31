const BASE_URL = 'http://localhost:8000/api'

export interface User {
  id: number
  username: string
  role: string
  full_name: string
  email: string
}

export interface Department {
  id: number
  name: string
  code: string
}

export interface Course {
  id: number
  title: string
  description: string | null
  capacity: number
  credits: number
  department_id: number
  teacher_id: number
  department?: Department
  teacher?: User
}

export interface Enrollment {
  id: number
  student_id: number
  course_id: number
  enrolled_at: string
  student?: User
  course?: Course
}

export interface Grade {
  id: number
  enrollment_id: number
  score: number
  letter_grade: string | null
  graded_at: string
  enrollment?: Enrollment
}

export interface Assignment {
  id: number
  course_id: number
  title: string
  description: string | null
  due_date: string
  max_score: number
  course?: Course
}

export interface Submission {
  id: number
  assignment_id: number
  student_id: number
  content: string | null
  submitted_at: string
  is_late: boolean
  student?: User
  assignment?: Assignment
}

async function request(url: string, options?: RequestInit) {
  const res = await fetch(BASE_URL + url, {
    headers: { 'Content-Type': 'application/json', ...options?.headers },
    ...options
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Request failed' }))
    throw new Error(err.detail || 'Request failed')
  }
  if (res.status === 204) return null
  return res.json()
}

// Auth
export const login = (username: string, password: string) =>
  request('/login', { method: 'POST', body: JSON.stringify({ username, password }) })

// Users
export const getUsers = () => request('/users')
export const getUser = (id: number) => request(`/users/${id}`)
export const createUser = (data: any) => request('/users', { method: 'POST', body: JSON.stringify(data) })
export const updateUser = (id: number, data: any) => request(`/users/${id}`, { method: 'PUT', body: JSON.stringify(data) })
export const deleteUser = (id: number) => request(`/users/${id}`, { method: 'DELETE' })

// Departments
export const getDepartments = () => request('/departments')
export const getDepartment = (id: number) => request(`/departments/${id}`)
export const createDepartment = (data: any) => request('/departments', { method: 'POST', body: JSON.stringify(data) })
export const updateDepartment = (id: number, data: any) => request(`/departments/${id}`, { method: 'PUT', body: JSON.stringify(data) })
export const deleteDepartment = (id: number) => request(`/departments/${id}`, { method: 'DELETE' })

// Courses
export const getCourses = () => request('/courses')
export const getCourse = (id: number) => request(`/courses/${id}`)
export const createCourse = (data: any) => request('/courses', { method: 'POST', body: JSON.stringify(data) })
export const updateCourse = (id: number, data: any) => request(`/courses/${id}`, { method: 'PUT', body: JSON.stringify(data) })
export const deleteCourse = (id: number) => request(`/courses/${id}`, { method: 'DELETE' })

// Enrollments
export const getEnrollments = () => request('/enrollments')
export const getEnrollment = (id: number) => request(`/enrollments/${id}`)
export const createEnrollment = (student_id: number, course_id: number) =>
  request('/enrollments', { method: 'POST', body: JSON.stringify({ student_id, course_id }) })
export const deleteEnrollment = (id: number) => request(`/enrollments/${id}`, { method: 'DELETE' })

// Grades
export const getGrades = () => request('/grades')
export const getGrade = (id: number) => request(`/grades/${id}`)
export const createGrade = (enrollment_id: number, score: number, letter_grade?: string) =>
  request('/grades', { method: 'POST', body: JSON.stringify({ enrollment_id, score, letter_grade }) })
export const updateGrade = (id: number, enrollment_id: number, score: number, letter_grade?: string) =>
  request(`/grades/${id}`, { method: 'PUT', body: JSON.stringify({ enrollment_id, score, letter_grade }) })

// Assignments
export const getAssignments = () => request('/assignments')
export const getAssignment = (id: number) => request(`/assignments/${id}`)
export const createAssignment = (data: any) => request('/assignments', { method: 'POST', body: JSON.stringify(data) })
export const updateAssignment = (id: number, data: any) => request(`/assignments/${id}`, { method: 'PUT', body: JSON.stringify(data) })
export const deleteAssignment = (id: number) => request(`/assignments/${id}`, { method: 'DELETE' })

// Submissions
export const getSubmissions = (assignmentId: number) => request(`/assignments/${assignmentId}/submissions`)
export const submitAssignment = (assignmentId: number, student_id: number, content?: string, submitted_at?: string) =>
  request(`/assignments/${assignmentId}/submissions`, { method: 'POST', body: JSON.stringify({ student_id, content, submitted_at }) })