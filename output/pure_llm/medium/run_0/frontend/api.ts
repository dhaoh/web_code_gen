const BASE_URL = 'http://localhost:8000/api';

async function request(url: string, options: RequestInit = {}) {
  const token = localStorage.getItem('token');
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options.headers as Record<string, string>),
  };
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  const response = await fetch(`${BASE_URL}${url}`, { ...options, headers });
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `Request failed: ${response.status}`);
  }
  if (response.status === 204) return null;
  return response.json();
}

// Auth
export async function apiLogin(username: string, password: string) {
  return request('/token', {
    method: 'POST',
    body: JSON.stringify({ username, password }),
  });
}

export async function apiGetCurrentUser(token: string) {
  const response = await fetch(`${BASE_URL}/users/me`, {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
  if (!response.ok) throw new Error('Failed to get user');
  return response.json();
}

// Users
export const apiListUsers = () => request('/users');
export const apiCreateUser = (data: any) => request('/users', { method: 'POST', body: JSON.stringify(data) });
export const apiUpdateUser = (id: number, data: any) => request(`/users/${id}`, { method: 'PUT', body: JSON.stringify(data) });
export const apiDeleteUser = (id: number) => request(`/users/${id}`, { method: 'DELETE' });

// Departments
export const apiListDepartments = () => request('/departments');
export const apiCreateDepartment = (data: any) => request('/departments', { method: 'POST', body: JSON.stringify(data) });
export const apiUpdateDepartment = (id: number, data: any) => request(`/departments/${id}`, { method: 'PUT', body: JSON.stringify(data) });
export const apiDeleteDepartment = (id: number) => request(`/departments/${id}`, { method: 'DELETE' });

// Courses
export const apiListCourses = (params?: Record<string, string>) => {
  const query = params ? new URLSearchParams(params).toString() : '';
  return request(`/courses${query ? '?' + query : ''}`);
};
export const apiCreateCourse = (data: any) => request('/courses', { method: 'POST', body: JSON.stringify(data) });
export const apiUpdateCourse = (id: number, data: any) => request(`/courses/${id}`, { method: 'PUT', body: JSON.stringify(data) });
export const apiDeleteCourse = (id: number) => request(`/courses/${id}`, { method: 'DELETE' });

// Enrollments
export const apiListEnrollments = (params?: Record<string, string>) => {
  const query = params ? new URLSearchParams(params).toString() : '';
  return request(`/enrollments${query ? '?' + query : ''}`);
};
export const apiCreateEnrollment = (data: any) => request('/enrollments', { method: 'POST', body: JSON.stringify(data) });
export const apiDeleteEnrollment = (id: number) => request(`/enrollments/${id}`, { method: 'DELETE' });

// Grades
export const apiListGrades = (params?: Record<string, string>) => {
  const query = params ? new URLSearchParams(params).toString() : '';
  return request(`/grades${query ? '?' + query : ''}`);
};
export const apiCreateGrade = (data: any) => request('/grades', { method: 'POST', body: JSON.stringify(data) });
export const apiUpdateGrade = (id: number, data: any) => request(`/grades/${id}`, { method: 'PUT', body: JSON.stringify(data) });

// Assignments
export const apiListAssignments = (params?: Record<string, string>) => {
  const query = params ? new URLSearchParams(params).toString() : '';
  return request(`/assignments${query ? '?' + query : ''}`);
};
export const apiCreateAssignment = (data: any) => request('/assignments', { method: 'POST', body: JSON.stringify(data) });
export const apiUpdateAssignment = (id: number, data: any) => request(`/assignments/${id}`, { method: 'PUT', body: JSON.stringify(data) });
export const apiDeleteAssignment = (id: number) => request(`/assignments/${id}`, { method: 'DELETE' });

// Submissions
export const apiListSubmissions = (params?: Record<string, string>) => {
  const query = params ? new URLSearchParams(params).toString() : '';
  return request(`/submissions${query ? '?' + query : ''}`);
};
export const apiCreateSubmission = (data: any) => request('/submissions', { method: 'POST', body: JSON.stringify(data) });