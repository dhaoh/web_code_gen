const API_BASE = 'http://localhost:8000/api';

// Student API
export interface Student {
  id: number;
  name: string;
  email: string;
}

export interface StudentCreate {
  name: string;
  email: string;
}

export interface StudentUpdate {
  name?: string;
  email?: string;
}

export async function getStudents(): Promise<Student[]> {
  const response = await fetch(`${API_BASE}/students/`);
  if (!response.ok) throw new Error('Failed to fetch students');
  return response.json();
}

export async function getStudent(id: number): Promise<Student> {
  const response = await fetch(`${API_BASE}/students/${id}`);
  if (!response.ok) throw new Error('Failed to fetch student');
  return response.json();
}

export async function createStudent(student: StudentCreate): Promise<Student> {
  const response = await fetch(`${API_BASE}/students/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(student),
  });
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to create student');
  }
  return response.json();
}

export async function updateStudent(id: number, student: StudentUpdate): Promise<Student> {
  const response = await fetch(`${API_BASE}/students/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(student),
  });
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to update student');
  }
  return response.json();
}

export async function deleteStudent(id: number): Promise<void> {
  const response = await fetch(`${API_BASE}/students/${id}`, {
    method: 'DELETE',
  });
  if (!response.ok) throw new Error('Failed to delete student');
}

// Course API
export interface Course {
  id: number;
  title: string;
  description: string | null;
  capacity: number;
  enrolled_count: number;
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

export async function getCourses(): Promise<Course[]> {
  const response = await fetch(`${API_BASE}/courses/`);
  if (!response.ok) throw new Error('Failed to fetch courses');
  return response.json();
}

export async function getCourse(id: number): Promise<Course> {
  const response = await fetch(`${API_BASE}/courses/${id}`);
  if (!response.ok) throw new Error('Failed to fetch course');
  return response.json();
}

export async function createCourse(course: CourseCreate): Promise<Course> {
  const response = await fetch(`${API_BASE}/courses/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(course),
  });
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to create course');
  }
  return response.json();
}

export async function updateCourse(id: number, course: CourseUpdate): Promise<Course> {
  const response = await fetch(`${API_BASE}/courses/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(course),
  });
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to update course');
  }
  return response.json();
}

export async function deleteCourse(id: number): Promise<void> {
  const response = await fetch(`${API_BASE}/courses/${id}`, {
    method: 'DELETE',
  });
  if (!response.ok) throw new Error('Failed to delete course');
}

// Enrollment API
export interface Enrollment {
  id: number;
  student_id: number;
  course_id: number;
  enrolled_at: string;
  student_name: string;
  course_title: string;
}

export interface EnrollmentCreate {
  student_id: number;
  course_id: number;
}

export async function getEnrollments(): Promise<Enrollment[]> {
  const response = await fetch(`${API_BASE}/enrollments/`);
  if (!response.ok) throw new Error('Failed to fetch enrollments');
  return response.json();
}

export async function getEnrollment(id: number): Promise<Enrollment> {
  const response = await fetch(`${API_BASE}/enrollments/${id}`);
  if (!response.ok) throw new Error('Failed to fetch enrollment');
  return response.json();
}

export async function createEnrollment(enrollment: EnrollmentCreate): Promise<Enrollment> {
  const response = await fetch(`${API_BASE}/enrollments/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(enrollment),
  });
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to create enrollment');
  }
  return response.json();
}

export async function deleteEnrollment(id: number): Promise<void> {
  const response = await fetch(`${API_BASE}/enrollments/${id}`, {
    method: 'DELETE',
  });
  if (!response.ok) throw new Error('Failed to delete enrollment');
}

export async function getStudentEnrollments(studentId: number): Promise<Enrollment[]> {
  const response = await fetch(`${API_BASE}/students/${studentId}/enrollments/`);
  if (!response.ok) throw new Error('Failed to fetch student enrollments');
  return response.json();
}

export async function getCourseEnrollments(courseId: number): Promise<Enrollment[]> {
  const response = await fetch(`${API_BASE}/courses/${courseId}/enrollments/`);
  if (!response.ok) throw new Error('Failed to fetch course enrollments');
  return response.json();
}