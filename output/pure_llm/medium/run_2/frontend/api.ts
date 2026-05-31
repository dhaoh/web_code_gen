const BASE_URL = 'http://localhost:8000/api';

async function request(path: string, options?: RequestInit) {
  const res = await fetch(BASE_URL + path, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  if (res.status === 204) return null;
  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(error.detail || 'Request failed');
  }
  return res.json();
}

export const api = {
  // Users
  getUsers: () => request('/users/'),
  getUser: (id: number) => request(`/users/${id}`),
  createUser: (data: any) => request('/users/', { method: 'POST', body: JSON.stringify(data) }),
  updateUser: (id: number, data: any) => request(`/users/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  deleteUser: (id: number) => request(`/users/${id}`, { method: 'DELETE' }),

  // Departments
  getDepartments: () => request('/departments/'),
  getDepartment: (id: number) => request(`/departments/${id}`),
  createDepartment: (data: any) => request('/departments/', { method: 'POST', body: JSON.stringify(data) }),
  updateDepartment: (id: number, data: any) => request(`/departments/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  deleteDepartment: (id: number) => request(`/departments/${id}`, { method: 'DELETE' }),

  // Courses
  getCourses: () => request('/courses/'),
  getCourse: (id: number) => request(`/courses/${id}`),
  createCourse: (data: any) => request('/courses/', { method: 'POST', body: JSON.stringify(data) }),
  updateCourse: (id: number, data: any) => request(`/courses/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  deleteCourse: (id: number) => request(`/courses/${id}`, { method: 'DELETE' }),

  // Enrollments
  getEnrollments: () => request('/enrollments/'),
  createEnrollment: (data: any) => request('/enrollments/', { method: 'POST', body: JSON.stringify(data) }),
  deleteEnrollment: (id: number) => request(`/enrollments/${id}`, { method: 'DELETE' }),

  // Grades
  getGrades: () => request('/grades/'),
  getGrade: (id: number) => request(`/grades/${id}`),
  createGrade: (data: any) => request('/grades/', { method: 'POST', body: JSON.stringify(data) }),
  updateGrade: (id: number, data: any) => request(`/grades/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  deleteGrade: (id: number) => request(`/grades/${id}`, { method: 'DELETE' }),

  // Assignments
  getAssignments: () => request('/assignments/'),
  getAssignment: (id: number) => request(`/assignments/${id}`),
  createAssignment: (data: any) => request('/assignments/', { method: 'POST', body: JSON.stringify(data) }),
  updateAssignment: (id: number, data: any) => request(`/assignments/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  deleteAssignment: (id: number) => request(`/assignments/${id}`, { method: 'DELETE' }),
};