const API_BASE = 'http://localhost:8000/api';

// Helper function for API calls
async function apiCall<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${endpoint}`, {
    headers: {
      'Content-Type': 'application/json',
    },
    ...options,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'An error occurred' }));
    throw new Error(error.detail || `HTTP error! status: ${response.status}`);
  }

  if (response.status === 204) {
    return {} as T;
  }

  return response.json();
}

// Student API
export interface Student {
  id: number;
  name: string;
  email: string;
  courses: Course[];
}

export interface StudentCreate {
  name: string;
  email: string;
}

export interface StudentUpdate {
  name?: string;
  email?: string;
}

export const studentApi = {
  getAll: () => apiCall<Student[]>('/students/'),
  getById: (id: number) => apiCall<Student>(`/students/${id}`),
  create: (data: StudentCreate) => apiCall<Student>('/students/', {
    method: 'POST',
    body: JSON.stringify(data),
  }),
  update: (id: number, data: StudentUpdate) => apiCall<Student>(`/students/${id}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  }),
  delete: (id: number) => apiCall<void>(`/students/${id}`, {
    method: 'DELETE',
  }),
};

// Course API
export interface Course {
  id: number;
  title: string;
  description?: string;
  capacity: number;
  students: Student[];
  enrollment_count: number;
}

export interface CourseCreate {
  title: string;
  description?: string;
  capacity: number;
}

export interface CourseUpdate {
  title?: string;
  description?: string;
  capacity?: number;
}

export const courseApi = {
  getAll: () => apiCall<Course[]>('/courses/'),
  getById: (id: number) => apiCall<Course>(`/courses/${id}`),
  create: (data: CourseCreate) => apiCall<Course>('/courses/', {
    method: 'POST',
    body: JSON.stringify(data),
  }),
  update: (id: number, data: CourseUpdate) => apiCall<Course>(`/courses/${id}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  }),
  delete: (id: number) => apiCall<void>(`/courses/${id}`, {
    method: 'DELETE',
  }),
};

// Enrollment API
export interface Enrollment {
  id: number;
  student_id: number;
  course_id: number;
  enrolled_at: string;
  student: Student;
  course: Course;
}

export interface EnrollmentCreate {
  student_id: number;
  course_id: number;
}

export const enrollmentApi = {
  getAll: () => apiCall<Enrollment[]>('/enrollments/'),
  getById: (id: number) => apiCall<Enrollment>(`/enrollments/${id}`),
  create: (data: EnrollmentCreate) => apiCall<Enrollment>('/enrollments/', {
    method: 'POST',
    body: JSON.stringify(data),
  }),
  delete: (id: number) => apiCall<void>(`/enrollments/${id}`, {
    method: 'DELETE',
  }),
};