const BASE_URL = 'http://localhost:8000/api';

export interface Student {
  id: number;
  name: string;
  email: string;
}

export interface Course {
  id: number;
  title: string;
  description?: string;
  capacity: number;
}

export interface Enrollment {
  id: number;
  student_id: number;
  course_id: number;
  enrolled_at: string;
  student_name: string;
  course_title: string;
}

export interface StudentCreate {
  name: string;
  email: string;
}

export interface CourseCreate {
  title: string;
  description?: string;
  capacity: number;
}

export interface EnrollmentCreate {
  student_id: number;
  course_id: number;
}

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Request failed');
  }
  if (response.status === 204) return {} as T;
  return response.json();
}

export async function getStudents(): Promise<Student[]> {
  const res = await fetch(`${BASE_URL}/students`);
  return handleResponse<Student[]>(res);
}

export async function getStudent(id: number): Promise<Student> {
  const res = await fetch(`${BASE_URL}/students/${id}`);
  return handleResponse<Student>(res);
}

export async function createStudent(data: StudentCreate): Promise<Student> {
  const res = await fetch(`${BASE_URL}/students`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  return handleResponse<Student>(res);
}

export async function updateStudent(id: number, data: StudentCreate): Promise<Student> {
  const res = await fetch(`${BASE_URL}/students/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  return handleResponse<Student>(res);
}

export async function deleteStudent(id: number): Promise<void> {
  const res = await fetch(`${BASE_URL}/students/${id}`, { method: 'DELETE' });
  return handleResponse<void>(res);
}

export async function getCourses(): Promise<Course[]> {
  const res = await fetch(`${BASE_URL}/courses`);
  return handleResponse<Course[]>(res);
}

export async function getCourse(id: number): Promise<Course> {
  const res = await fetch(`${BASE_URL}/courses/${id}`);
  return handleResponse<Course>(res);
}

export async function createCourse(data: CourseCreate): Promise<Course> {
  const res = await fetch(`${BASE_URL}/courses`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  return handleResponse<Course>(res);
}

export async function updateCourse(id: number, data: CourseCreate): Promise<Course> {
  const res = await fetch(`${BASE_URL}/courses/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  return handleResponse<Course>(res);
}

export async function deleteCourse(id: number): Promise<void> {
  const res = await fetch(`${BASE_URL}/courses/${id}`, { method: 'DELETE' });
  return handleResponse<void>(res);
}

export async function getEnrollments(): Promise<Enrollment[]> {
  const res = await fetch(`${BASE_URL}/enrollments`);
  return handleResponse<Enrollment[]>(res);
}

export async function createEnrollment(data: EnrollmentCreate): Promise<Enrollment> {
  const res = await fetch(`${BASE_URL}/enrollments`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  return handleResponse<Enrollment>(res);
}

export async function deleteEnrollment(id: number): Promise<void> {
  const res = await fetch(`${BASE_URL}/enrollments/${id}`, { method: 'DELETE' });
  return handleResponse<void>(res);
}