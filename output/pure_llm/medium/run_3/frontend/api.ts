const BASE_URL = "http://localhost:8000";

let token: string | null = localStorage.getItem("token");

export function setToken(newToken: string | null) {
  token = newToken;
  if (newToken) localStorage.setItem("token", newToken);
  else localStorage.removeItem("token");
}

function headers(): HeadersInit {
  const h: HeadersInit = { "Content-Type": "application/json" };
  if (token) h["Authorization"] = `Bearer ${token}`;
  return h;
}

async function request(path: string, options?: RequestInit) {
  const res = await fetch(`${BASE_URL}${path}`, {
    ...options,
    headers: { ...headers(), ...options?.headers },
  });
  if (res.status === 204) return null;
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || "Request failed");
  return data;
}

export const api = {
  // Auth
  login: (username: string, password: string) =>
    request("/login", {
      method: "POST",
      body: JSON.stringify({ username, password }),
    }),
  register: (user: {
    username: string;
    password: string;
    role: string;
    full_name: string;
    email: string;
  }) =>
    request("/register", {
      method: "POST",
      body: JSON.stringify(user),
    }),
  getMe: () => request("/users/me"),
  // Users
  getUsers: (role?: string) =>
    request(`/users${role ? `?role=${role}` : ""}`),
  getUser: (id: number) => request(`/users/${id}`),
  updateUser: (id: number, data: any) =>
    request(`/users/${id}`, {
      method: "PUT",
      body: JSON.stringify(data),
    }),
  deleteUser: (id: number) =>
    request(`/users/${id}`, { method: "DELETE" }),
  // Departments
  getDepartments: () => request("/departments"),
  createDepartment: (data: { name: string; code: string }) =>
    request("/departments", {
      method: "POST",
      body: JSON.stringify(data),
    }),
  getDepartment: (id: number) => request(`/departments/${id}`),
  updateDepartment: (id: number, data: { name: string; code: string }) =>
    request(`/departments/${id}`, {
      method: "PUT",
      body: JSON.stringify(data),
    }),
  deleteDepartment: (id: number) =>
    request(`/departments/${id}`, { method: "DELETE" }),
  // Courses
  getCourses: () => request("/courses"),
  createCourse: (data: any) =>
    request("/courses", { method: "POST", body: JSON.stringify(data) }),
  getCourse: (id: number) => request(`/courses/${id}`),
  updateCourse: (id: number, data: any) =>
    request(`/courses/${id}`, {
      method: "PUT",
      body: JSON.stringify(data),
    }),
  deleteCourse: (id: number) =>
    request(`/courses/${id}`, { method: "DELETE" }),
  // Enrollments
  getEnrollments: () => request("/enrollments"),
  createEnrollment: (course_id: number) =>
    request("/enrollments", {
      method: "POST",
      body: JSON.stringify({ course_id }),
    }),
  getEnrollment: (id: number) => request(`/enrollments/${id}`),
  deleteEnrollment: (id: number) =>
    request(`/enrollments/${id}`, { method: "DELETE" }),
  // Grades
  getGrades: () => request("/grades"),
  createGrade: (enrollment_id: number, score: number) =>
    request("/grades", {
      method: "POST",
      body: JSON.stringify({ enrollment_id, score }),
    }),
  getGrade: (id: number) => request(`/grades/${id}`),
  updateGrade: (id: number, score: number) =>
    request(`/grades/${id}`, {
      method: "PUT",
      body: JSON.stringify({ score }),
    }),
  deleteGrade: (id: number) =>
    request(`/grades/${id}`, { method: "DELETE" }),
  // Assignments
  getAssignments: (course_id?: number) =>
    request(`/assignments${course_id ? `?course_id=${course_id}` : ""}`),
  createAssignment: (data: any) =>
    request("/assignments", {
      method: "POST",
      body: JSON.stringify(data),
    }),
  getAssignment: (id: number) => request(`/assignments/${id}`),
  updateAssignment: (id: number, data: any) =>
    request(`/assignments/${id}`, {
      method: "PUT",
      body: JSON.stringify(data),
    }),
  deleteAssignment: (id: number) =>
    request(`/assignments/${id}`, { method: "DELETE" }),
};