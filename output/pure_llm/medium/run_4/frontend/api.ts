// API client

const API_BASE = "http://localhost:8000/api";

async function request<T>(url: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${url}`, {
    headers: {
      "Content-Type": "application/json",
    },
    ...options,
  });
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: "Unknown error" }));
    throw new Error(error.detail || "Request failed");
  }
  return response.json();
}

// Types
export interface User {
  id: number;
  username: string;
  role: string;
  full_name: string;
  email: string;
  password_hash?: string; // not used on frontend
}

export interface UserCreate {
  username: string;
  password: string;
  role: string;
  full_name: string;
  email: string;
}

export interface UserUpdate {
  full_name?: string;
  email?: string;
  role?: string;
}

export interface Department {
  id: number;
  name: string;
  code: string;
}

export interface DepartmentCreate {
  name: string;
  code: string;
}

export interface Course {
  id: number;
  title: string;
  description?: string;
  capacity: number;
  credits: number;
  department_id: number;
  teacher_id?: number;
}

export interface CourseCreate {
  title: string;
  description?: string;
  capacity: number;
  credits: number;
  department_id: number;
  teacher_id?: number;
}

export interface CourseUpdate {
  title?: string;
  description?: string;
  capacity?: number;
  credits?: number;
  department_id?: number;
  teacher_id?: number;
}

export interface Enrollment {
  id: number;
  student_id: number;
  course_id: number;
  enrolled_at: string;
}

export interface EnrollmentCreate {
  student_id: number;
  course_id: number;
}

export interface Grade {
  id: number;
  enrollment_id: number;
  score: number;
  letter_grade?: string;
  graded_at?: string;
}

export interface GradeCreate {
  enrollment_id: number;
  score: number;
}

export interface Assignment {
  id: number;
  course_id: number;
  title: string;
  description?: string;
  due_date: string;
  max_score: number;
}

export interface AssignmentCreate {
  course_id: number;
  title: string;
  description?: string;
  due_date: string;
  max_score: number;
}

// Users
export const getUsers = () => request<User[]>("/users");
export const getUser = (id: number) => request<User>(`/users/${id}`);
export const createUser = (data: UserCreate) => request<User>("/users", { method: "POST", body: JSON.stringify(data) });
export const updateUser = (id: number, data: UserUpdate) => request<User>(`/users/${id}`, { method: "PUT", body: JSON.stringify(data) });
export const deleteUser = (id: number) => request<{ detail: string }>(`/users/${id}`, { method: "DELETE" });

// Departments
export const getDepartments = () => request<Department[]>("/departments");
export const getDepartment = (id: number) => request<Department>(`/departments/${id}`);
export const createDepartment = (data: DepartmentCreate) => request<Department>("/departments", { method: "POST", body: JSON.stringify(data) });
export const updateDepartment = (id: number, data: DepartmentCreate) => request<Department>(`/departments/${id}`, { method: "PUT", body: JSON.stringify(data) });
export const deleteDepartment = (id: number) => request<{ detail: string }>(`/departments/${id}`, { method: "DELETE" });

// Courses
export const getCourses = () => request<Course[]>("/courses");
export const getCourse = (id: number) => request<Course>(`/courses/${id}`);
export const createCourse = (data: CourseCreate) => request<Course>("/courses", { method: "POST", body: JSON.stringify(data) });
export const updateCourse = (id: number, data: CourseUpdate) => request<Course>(`/courses/${id}`, { method: "PUT", body: JSON.stringify(data) });
export const deleteCourse = (id: number) => request<{ detail: string }>(`/courses/${id}`, { method: "DELETE" });

// Enrollments
export const getEnrollments = () => request<Enrollment[]>("/enrollments");
export const getEnrollment = (id: number) => request<Enrollment>(`/enrollments/${id}`);
export const createEnrollment = (data: EnrollmentCreate) => request<Enrollment>("/enrollments", { method: "POST", body: JSON.stringify(data) });
export const deleteEnrollment = (id: number) => request<{ detail: string }>(`/enrollments/${id}`, { method: "DELETE" });

// Grades
export const getGrades = () => request<Grade[]>("/grades");
export const getGrade = (id: number) => request<Grade>(`/grades/${id}`);
export const createGrade = (data: GradeCreate) => request<Grade>("/grades", { method: "POST", body: JSON.stringify(data) });
export const updateGrade = (id: number, data: GradeCreate) => request<Grade>(`/grades/${id}`, { method: "PUT", body: JSON.stringify(data) });
export const deleteGrade = (id: number) => request<{ detail: string }>(`/grades/${id}`, { method: "DELETE" });

// Assignments
export const getAssignments = () => request<Assignment[]>("/assignments");
export const getAssignment = (id: number) => request<Assignment>(`/assignments/${id}`);
export const createAssignment = (data: AssignmentCreate) => request<Assignment>("/assignments", { method: "POST", body: JSON.stringify(data) });
export const updateAssignment = (id: number, data: AssignmentCreate) => request<Assignment>(`/assignments/${id}`, { method: "PUT", body: JSON.stringify(data) });
export const deleteAssignment = (id: number) => request<{ detail: string }>(`/assignments/${id}`, { method: "DELETE" });