const API_BASE = "http://localhost:8000/api";

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
}

// Students
export async function fetchStudents(): Promise<Student[]> {
  const res = await fetch(`${API_BASE}/students/`);
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function fetchStudent(id: number): Promise<Student> {
  const res = await fetch(`${API_BASE}/students/${id}`);
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function createStudent(data: Omit<Student, "id">): Promise<Student> {
  const res = await fetch(`${API_BASE}/students/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function updateStudent(id: number, data: Omit<Student, "id">): Promise<Student> {
  const res = await fetch(`${API_BASE}/students/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function deleteStudent(id: number): Promise<void> {
  const res = await fetch(`${API_BASE}/students/${id}`, { method: "DELETE" });
  if (!res.ok) throw new Error(await res.text());
}

// Courses
export async function fetchCourses(): Promise<Course[]> {
  const res = await fetch(`${API_BASE}/courses/`);
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function fetchCourse(id: number): Promise<Course> {
  const res = await fetch(`${API_BASE}/courses/${id}`);
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function createCourse(data: Omit<Course, "id">): Promise<Course> {
  const res = await fetch(`${API_BASE}/courses/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function updateCourse(id: number, data: Omit<Course, "id">): Promise<Course> {
  const res = await fetch(`${API_BASE}/courses/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function deleteCourse(id: number): Promise<void> {
  const res = await fetch(`${API_BASE}/courses/${id}`, { method: "DELETE" });
  if (!res.ok) throw new Error(await res.text());
}

// Enrollments
export async function fetchEnrollments(): Promise<Enrollment[]> {
  const res = await fetch(`${API_BASE}/enrollments/`);
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function createEnrollment(student_id: number, course_id: number): Promise<Enrollment> {
  const res = await fetch(`${API_BASE}/enrollments/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ student_id, course_id }),
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function deleteEnrollment(id: number): Promise<void> {
  const res = await fetch(`${API_BASE}/enrollments/${id}`, { method: "DELETE" });
  if (!res.ok) throw new Error(await res.text());
}