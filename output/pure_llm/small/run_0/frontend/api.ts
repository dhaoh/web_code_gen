const BASE_URL = 'http://localhost:8000';

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
  enrolled_count: number;
}

export interface Enrollment {
  id: number;
  student_id: number;
  course_id: number;
  enrolled_at: string;
  student_name: string;
  course_title: string;
}

// Students
export async function fetchStudents(): Promise<Student[]> {
  const res = await fetch(`${BASE_URL}/students`);
  if (!res.ok) throw new Error(`Failed to fetch students: ${res.statusText}`);
  return res.json();
}

export async function fetchStudent(id: number): Promise<Student> {
  const res = await fetch(`${BASE_URL}/students/${id}`);
  if (!res.ok) throw new Error(`Failed to fetch student: ${res.statusText}`);
  return res.json();
}

export async function createStudent(data: { name: string; email: string }): Promise<Student> {
  const res = await fetch(`${BASE_URL}/students`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || 'Failed to create student');
  }
  return res.json();
}

export async function updateStudent(id: number, data: { name?: string; email?: string }): Promise<Student> {
  const res = await fetch(`${BASE_URL}/students/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || 'Failed to update student');
  }
  return res.json();
}

export async function deleteStudent(id: number): Promise<void> {
  const res = await fetch(`${BASE_URL}/students/${id}`, { method: 'DELETE' });
  if (!res.ok) throw new Error('Failed to delete student');
}

// Courses
export async function fetchCourses(): Promise<Course[]> {
  const res = await fetch(`${BASE_URL}/courses`);
  if (!res.ok) throw new Error('Failed to fetch courses');
  return res.json();
}

export async function fetchCourse(id: number): Promise<Course> {
  const res = await fetch(`${BASE_URL}/courses/${id}`);
  if (!res.ok) throw new Error('Failed to fetch course');
  return res.json();
}

export async function createCourse(data: { title: string; description?: string; capacity: number }): Promise<Course> {
  const res = await fetch(`${BASE_URL}/courses`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || 'Failed to create course');
  }
  return res.json();
}

export async function updateCourse(id: number, data: { title?: string; description?: string; capacity?: number }): Promise<Course> {
  const res = await fetch(`${BASE_URL}/courses/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || 'Failed to update course');
  }
  return res.json();
}

export async function deleteCourse(id: number): Promise<void> {
  const res = await fetch(`${BASE_URL}/courses/${id}`, { method: 'DELETE' });
  if (!res.ok) throw new Error('Failed to delete course');
}

// Enrollments
export async function fetchEnrollments(filters?: { student_id?: number; course_id?: number }): Promise<Enrollment[]> {
  let url = `${BASE_URL}/enrollments`;
  const params = new URLSearchParams();
  if (filters?.student_id) params.append('student_id', String(filters.student_id));
  if (filters?.course_id) params.append('course_id', String(filters.course_id));
  const qs = params.toString();
  if (qs) url += `?${qs}`;
  const res = await fetch(url);
  if (!res.ok) throw new Error('Failed to fetch enrollments');
  return res.json();
}

export async function createEnrollment(data: { student_id: number; course_id: number }): Promise<Enrollment> {
  const res = await fetch(`${BASE_URL}/enrollments`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || 'Failed to enroll');
  }
  return res.json();
}

export async function deleteEnrollment(id: number): Promise<void> {
  const res = await fetch(`${BASE_URL}/enrollments/${id}`, { method: 'DELETE' });
  if (!res.ok) throw new Error('Failed to drop enrollment');
}