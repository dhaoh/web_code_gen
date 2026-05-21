const BASE_URL = '/api';

interface Student {
  id: number;
  name: string;
  email: string;
}

interface Course {
  id: number;
  title: string;
  description?: string;
  capacity: number;
}

interface Enrollment {
  id: number;
  student_id: number;
  course_id: number;
  enrolled_at: string;
  student: Student;
  course: Course;
}

// Students
export async function fetchStudents(): Promise<Student[]> {
  const res = await fetch(`${BASE_URL}/students`);
  if (!res.ok) throw new Error('Failed to fetch students');
  return res.json();
}

export async function getStudent(id: number): Promise<Student> {
  const res = await fetch(`${BASE_URL}/students/${id}`);
  if (!res.ok) throw new Error('Student not found');
  return res.json();
}

export async function createStudent(data: Omit<Student, 'id'>): Promise<Student> {
  const res = await fetch(`${BASE_URL}/students`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || 'Failed to create student');
  }
  return res.json();
}

export async function updateStudent(id: number, data: Partial<Omit<Student, 'id'>>): Promise<Student> {
  const res = await fetch(`${BASE_URL}/students/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!res.ok) {
    const err = await res.json();
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

export async function getCourse(id: number): Promise<Course> {
  const res = await fetch(`${BASE_URL}/courses/${id}`);
  if (!res.ok) throw new Error('Course not found');
  return res.json();
}

export async function createCourse(data: Omit<Course, 'id'>): Promise<Course> {
  const res = await fetch(`${BASE_URL}/courses`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || 'Failed to create course');
  }
  return res.json();
}

export async function updateCourse(id: number, data: Partial<Omit<Course, 'id'>>): Promise<Course> {
  const res = await fetch(`${BASE_URL}/courses/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || 'Failed to update course');
  }
  return res.json();
}

export async function deleteCourse(id: number): Promise<void> {
  const res = await fetch(`${BASE_URL}/courses/${id}`, { method: 'DELETE' });
  if (!res.ok) throw new Error('Failed to delete course');
}

// Enrollments
export async function fetchEnrollments(): Promise<Enrollment[]> {
  const res = await fetch(`${BASE_URL}/enrollments`);
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
    const err = await res.json();
    throw new Error(err.detail || 'Failed to create enrollment');
  }
  return res.json();
}

export async function deleteEnrollment(id: number): Promise<void> {
  const res = await fetch(`${BASE_URL}/enrollments/${id}`, { method: 'DELETE' });
  if (!res.ok) throw new Error('Failed to delete enrollment');
}