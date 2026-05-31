const API_BASE = "http://localhost:8000/api";

let token: string | null = localStorage.getItem("token");

function authHeaders(): Record<string, string> {
  if (!token) return {};
  return { Authorization: `Bearer ${token}` };
}

async function request(path: string, options: RequestInit = {}) {
  const res = await fetch(API_BASE + path, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...authHeaders(),
      ...options.headers,
    },
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Request failed" }));
    throw new Error(err.detail || "Error");
  }
  return res.json();
}

export const api = {
  setToken(t: string | null) {
    token = t;
    if (t) localStorage.setItem("token", t);
    else localStorage.removeItem("token");
  },
  getToken() { return token; },
  login: (username: string, password: string) =>
    request("/auth/login", {
      method: "POST",
      body: JSON.stringify({ username, password }),
    }),

  // Users
  getUsers: () => request("/users"),
  createUser: (data: any) => request("/users", { method: "POST", body: JSON.stringify(data) }),
  updateUser: (id: number, data: any) => request(`/users/${id}`, { method: "PUT", body: JSON.stringify(data) }),
  deleteUser: (id: number) => request(`/users/${id}`, { method: "DELETE" }),

  // Departments
  getDepartments: () => request("/departments"),
  createDepartment: (data: any) => request("/departments", { method: "POST", body: JSON.stringify(data) }),
  updateDepartment: (id: number, data: any) => request(`/departments/${id}`, { method: "PUT", body: JSON.stringify(data) }),
  deleteDepartment: (id: number) => request(`/departments/${id}`, { method: "DELETE" }),

  // Majors
  getMajors: () => request("/majors"),
  createMajor: (data: any) => request("/majors", { method: "POST", body: JSON.stringify(data) }),
  updateMajor: (id: number, data: any) => request(`/majors/${id}`, { method: "PUT", body: JSON.stringify(data) }),
  deleteMajor: (id: number) => request(`/majors/${id}`, { method: "DELETE" }),

  // Courses
  getCourses: () => request("/courses"),
  createCourse: (data: any) => request("/courses", { method: "POST", body: JSON.stringify(data) }),
  updateCourse: (id: number, data: any) => request(`/courses/${id}`, { method: "PUT", body: JSON.stringify(data) }),
  deleteCourse: (id: number) => request(`/courses/${id}`, { method: "DELETE" }),

  // Prerequisites
  getPrerequisites: () => request("/prerequisites"),
  createPrerequisite: (data: any) => request("/prerequisites", { method: "POST", body: JSON.stringify(data) }),
  updatePrerequisite: (id: number, data: any) => request(`/prerequisites/${id}`, { method: "PUT", body: JSON.stringify(data) }),
  deletePrerequisite: (id: number) => request(`/prerequisites/${id}`, { method: "DELETE" }),

  // Classrooms
  getClassrooms: () => request("/classrooms"),
  createClassroom: (data: any) => request("/classrooms", { method: "POST", body: JSON.stringify(data) }),
  updateClassroom: (id: number, data: any) => request(`/classrooms/${id}`, { method: "PUT", body: JSON.stringify(data) }),
  deleteClassroom: (id: number) => request(`/classrooms/${id}`, { method: "DELETE" }),

  // Schedules
  getSchedules: () => request("/schedules"),
  createSchedule: (data: any) => request("/schedules", { method: "POST", body: JSON.stringify(data) }),
  updateSchedule: (id: number, data: any) => request(`/schedules/${id}`, { method: "PUT", body: JSON.stringify(data) }),
  deleteSchedule: (id: number) => request(`/schedules/${id}`, { method: "DELETE" }),

  // Enrollments
  getEnrollments: () => request("/enrollments"),
  createEnrollment: (data: { course_id: number }) => request("/enrollments", { method: "POST", body: JSON.stringify(data) }),
  dropEnrollment: (id: number) => request(`/enrollments/${id}/drop`, { method: "PUT" }),

  // Grades
  getGrades: () => request("/grades"),
  createGrade: (data: any) => request("/grades", { method: "POST", body: JSON.stringify(data) }),

  // Assignments
  getAssignments: () => request("/assignments"),
  createAssignment: (data: any) => request("/assignments", { method: "POST", body: JSON.stringify(data) }),
  updateAssignment: (id: number, data: any) => request(`/assignments/${id}`, { method: "PUT", body: JSON.stringify(data) }),
  deleteAssignment: (id: number) => request(`/assignments/${id}`, { method: "DELETE" }),
};