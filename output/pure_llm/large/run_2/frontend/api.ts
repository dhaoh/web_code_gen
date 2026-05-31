const API_BASE = "http://localhost:8000";

export async function apiRequest(path: string, options: RequestInit = {}) {
  const token = localStorage.getItem("token");
  const headers: Record<string,string> = {
    "Content-Type": "application/json",
    ...(options.headers as Record<string,string>),
  };
  if (token) headers["Authorization"] = `Bearer ${token}`;
  const res = await fetch(`${API_BASE}${path}`, { ...options, headers });
  if (!res.ok) {
    const error = await res.text();
    throw new Error(error || res.statusText);
  }
  return res.json();
}

// Auth
export const login = (username: string, password: string) =>
  apiRequest("/token", {
    method: "POST",
    body: JSON.stringify({ username, password }),
  });

// Users
export const getUsers = () => apiRequest("/users");
export const getUser = (id: number) => apiRequest(`/users/${id}`);
export const createUser = (data: any) =>
  apiRequest("/users", { method: "POST", body: JSON.stringify(data) });
export const updateUser = (id: number, data: any) =>
  apiRequest(`/users/${id}`, { method: "PUT", body: JSON.stringify(data) });
export const deleteUser = (id: number) =>
  apiRequest(`/users/${id}`, { method: "DELETE" });

// Departments
export const getDepartments = () => apiRequest("/departments");
export const createDepartment = (data: any) =>
  apiRequest("/departments", { method: "POST", body: JSON.stringify(data) });
// ...

// For simplicity, we'll reuse generic endpoints that we'll implement fully in pages.
// The actual api.ts can be generated with all CRUD functions.
// I'll provide a compact version with generic helpers:

export const list = (resource: string) => apiRequest(`/${resource}`);
export const getOne = (resource: string, id: number) => apiRequest(`/${resource}/${id}`);
export const create = (resource: string, data: any) =>
  apiRequest(`/${resource}`, { method: "POST", body: JSON.stringify(data) });
export const update = (resource: string, id: number, data: any) =>
  apiRequest(`/${resource}/${id}`, { method: "PUT", body: JSON.stringify(data) });
export const remove = (resource: string, id: number) =>
  apiRequest(`/${resource}/${id}`, { method: "DELETE" });

// Special endpoints
export const enroll = (studentId: number, courseId: number) =>
  apiRequest("/enrollments/enroll", {
    method: "POST",
    body: JSON.stringify({ student_id: studentId, course_id: courseId, status: "enrolled" }),
  });
export const createGrade = (data: any) =>
  apiRequest("/grades/", { method: "POST", body: JSON.stringify(data) });
export const submitAssignment = (data: any) =>
  apiRequest("/submissions/", { method: "POST", body: JSON.stringify(data) });
export const gradeSubmission = (subId: number, score: number) =>
  apiRequest(`/submissions/${subId}/grade?score=${score}`, { method: "PUT" });
export const majorProgress = (studentId: number) => apiRequest(`/students/${studentId}/major_progress`);