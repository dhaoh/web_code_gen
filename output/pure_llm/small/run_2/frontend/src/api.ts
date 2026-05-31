const BASE_URL = 'http://localhost:8000';

async function request<T>(url: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE_URL}${url}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(error.detail || `Request failed: ${res.status}`);
  }
  if (res.status === 204) return undefined as unknown as T;
  return res.json();
}

// Students
export interface Student {
  id: number;
  name: string;
  email: string;
}

export const fetchStudents = () => request<Student[]>('/students');
export const fetchStudent = (id: number) => request<Student>(`/students/${id}`);
export const createStudent = (data: { name: string; email: string }) =>
  request<Student>('/students', { method: 'POST', body: JSON.stringify(data) });
export const updateStudent = (id: number, data: { name: string; email: string }) =>
  request<Student>(`/students/${id}`, { method: 'PUT', body: JSON.stringify(data) });
export const deleteStudent = (id: number) =>
  request<void>(`/students/${id}`, { method: 'DELETE' });

// Courses
export interface Course {
  id: number;
  title: string;
  description: string | null;
  capacity: number;
  enrolled_count: number;
}

export const fetchCourses = () => request<Course[]>('/courses');
export const fetchCourse = (id: number) => request<Course>(`/courses/${id}`);
export const createCourse = (data: { title: string; description?: string; capacity: number }) =>
  request<Course>('/courses', { method: 'POST', body: JSON.stringify(data) });
export const updateCourse = (id: number, data: { title: string; description?: string; capacity: number }) =>
  request<Course>(`/courses/${id}`, { method: 'PUT', body: JSON.stringify(data) });
export const deleteCourse = (id: number) =>
  request<void>(`/courses/${id}`, { method: 'DELETE' });

// Enrollments
export interface Enrollment {
  id: number;
  student_id: number;
  course_id: number;
  enrolled_at: string;
  student: Student;
  course: Course;
}

export const fetchEnrollments = (student_id?: number) =>
  request<Enrollment[]>(`/enrollments${student_id ? `?student_id=${student_id}` : ''}`);
export const createEnrollment = (data: { student_id: number; course_id: number }) =>
  request<Enrollment>('/enrollments', { method: 'POST', body: JSON.stringify(data) });
export const deleteEnrollment = (id: number) =>
  request<void>(`/enrollments/${id}`, { method: 'DELETE' });