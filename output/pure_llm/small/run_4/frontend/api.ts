const API_BASE = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api';

async function apiRequest<T>(url: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${url}`, {
    headers: {
      'Content-Type': 'application/json',
    },
    ...options,
  });
  if (!response.ok) {
    let errorMessage = 'An error occurred';
    try {
      const errorData = await response.json();
      errorMessage = errorData.detail || errorMessage;
    } catch {}
    throw new Error(errorMessage);
  }
  if (response.status === 204) {
    return null as any;
  }
  return response.json();
}

// Student API
export const fetchStudents = () => apiRequest<any[]>('/students');
export const fetchStudent = (id: number) => apiRequest<any>(`/students/${id}`);
export const createStudent = (data: { name: string; email: string }) =>
  apiRequest<any>('/students', { method: 'POST', body: JSON.stringify(data) });
export const updateStudent = (id: number, data: { name: string; email: string }) =>
  apiRequest<any>(`/students/${id}`, { method: 'PUT', body: JSON.stringify(data) });
export const deleteStudent = (id: number) =>
  apiRequest<void>(`/students/${id}`, { method: 'DELETE' });

// Course API
export const fetchCourses = () => apiRequest<any[]>('/courses');
export const fetchCourse = (id: number) => apiRequest<any>(`/courses/${id}`);
export const createCourse = (data: { title: string; description?: string; capacity: number }) =>
  apiRequest<any>('/courses', { method: 'POST', body: JSON.stringify(data) });
export const updateCourse = (id: number, data: { title: string; description?: string; capacity: number }) =>
  apiRequest<any>(`/courses/${id}`, { method: 'PUT', body: JSON.stringify(data) });
export const deleteCourse = (id: number) =>
  apiRequest<void>(`/courses/${id}`, { method: 'DELETE' });

// Enrollment API
export const fetchEnrollments = (params?: { student_id?: number; course_id?: number }) => {
  const query = new URLSearchParams();
  if (params?.student_id) query.append('student_id', String(params.student_id));
  if (params?.course_id) query.append('course_id', String(params.course_id));
  const queryString = query.toString();
  return apiRequest<any[]>(`/enrollments${queryString ? `?${queryString}` : ''}`);
};
export const createEnrollment = (data: { student_id: number; course_id: number }) =>
  apiRequest<any>('/enrollments', { method: 'POST', body: JSON.stringify(data) });
export const deleteEnrollment = (id: number) =>
  apiRequest<void>(`/enrollments/${id}`, { method: 'DELETE' });