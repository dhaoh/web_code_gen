const API_BASE_URL = 'http://localhost:8000';

// Generic fetch wrapper with error handling
async function fetchAPI<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    headers: {
      'Content-Type': 'application/json',
    },
    ...options,
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return response.json();
}

// Student API
export interface Student {
  id: number;
  name: string;
  email: string;
  courses?: Course[];
}

export interface StudentCreate {
  name: string;
  email: string;
}

export interface StudentUpdate {
  name?: string;
  email?: string;
}

export const studentAPI = {
  getAll: () => fetchAPI<Student[]>('/students/'),
  getById: (id: number) => fetchAPI<Student>(`/students/${id}`),
  create: (data: StudentCreate) => fetchAPI<Student>('/students/', {
    method: 'POST',
    body: JSON.stringify(data),
  }),
  update: (id: number, data: StudentUpdate) => fetchAPI<Student>(`/students/${id}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  }),
  delete: (id: number) => fetchAPI<void>(`/students/${id}`, {
    method: 'DELETE',
  }),
};

// Course API
export interface Course {
  id: number;
  title: string;
  description?: string;
  capacity: number;
  enrolled_count?: number;
  students?: Student[];
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

export const courseAPI = {
  getAll: () => fetchAPI<Course[]>('/courses/'),
  getById: (id: number) => fetchAPI<Course>(`/courses/${id}`),
  create: (data: CourseCreate) => fetchAPI<Course>('/courses/', {
    method: 'POST',
    body: JSON.stringify(data),
  }),
  update: (id: number, data: CourseUpdate) => fetchAPI<Course>(`/courses/${id}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  }),
  delete: (id: number) => fetchAPI<void>(`/courses/${id}`, {
    method: 'DELETE',
  }),
};

// Enrollment API
export interface Enrollment {
  id: number;
  student_id: number;
  course_id: number;
  enrolled_at: string;
  student?: Student;
  course?: Course;
}

export interface EnrollmentCreate {
  student_id: number;
  course_id: number;
}

export const enrollmentAPI = {
  getAll: () => fetchAPI<Enrollment[]>('/enrollments/'),
  getById: (id: number) => fetchAPI<Enrollment>(`/enrollments/${id}`),
  create: (data: EnrollmentCreate) => fetchAPI<Enrollment>('/enrollments/', {
    method: 'POST',
    body: JSON.stringify(data),
  }),
  delete: (id: number) => fetchAPI<void>(`/enrollments/${id}`, {
    method: 'DELETE',
  }),
  getByStudent: (studentId: number) => fetchAPI<Enrollment[]>(`/students/${studentId}/enrollments/`),
  getByCourse: (courseId: number) => fetchAPI<Enrollment[]>(`/courses/${courseId}/enrollments/`),
};