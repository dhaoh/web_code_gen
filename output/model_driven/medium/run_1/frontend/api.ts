// Auto-generated API client for student_course_system_medium

const BASE_URL = 'http://localhost:8000';

// ==========================================
// User API
// ==========================================
export async function fetchUsers(): Promise<any[]> {
    const res = await fetch(`${BASE_URL}/users`);
    if (!res.ok) throw new Error(`Failed to fetch users: ${res.status}`);
    return res.json();
}

export async function fetchUser(id: number): Promise<any> {
    const res = await fetch(`${BASE_URL}/users/${id}`);
    if (!res.ok) throw new Error(`Failed to fetch User: ${res.status}`);
    return res.json();
}

export async function createUser(data: any): Promise<any> {
    const res = await fetch(`${BASE_URL}/users`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
    });
    if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: `HTTP ${res.status}` }));
        throw new Error(err.detail || `Failed to create User`);
    }
    return res.json();
}

export async function updateUser(id: number, data: any): Promise<any> {
    const res = await fetch(`${BASE_URL}/users/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
    });
    if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: `HTTP ${res.status}` }));
        throw new Error(err.detail || `Failed to update User`);
    }
    return res.json();
}

export async function deleteUser(id: number): Promise<void> {
    const res = await fetch(`${BASE_URL}/users/${id}`, {
        method: 'DELETE',
    });
    if (!res.ok) throw new Error(`Failed to delete User: ${res.status}`);
}

// ==========================================
// Department API
// ==========================================
export async function fetchDepartments(): Promise<any[]> {
    const res = await fetch(`${BASE_URL}/departments`);
    if (!res.ok) throw new Error(`Failed to fetch departments: ${res.status}`);
    return res.json();
}

export async function fetchDepartment(id: number): Promise<any> {
    const res = await fetch(`${BASE_URL}/departments/${id}`);
    if (!res.ok) throw new Error(`Failed to fetch Department: ${res.status}`);
    return res.json();
}

export async function createDepartment(data: any): Promise<any> {
    const res = await fetch(`${BASE_URL}/departments`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
    });
    if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: `HTTP ${res.status}` }));
        throw new Error(err.detail || `Failed to create Department`);
    }
    return res.json();
}

export async function updateDepartment(id: number, data: any): Promise<any> {
    const res = await fetch(`${BASE_URL}/departments/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
    });
    if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: `HTTP ${res.status}` }));
        throw new Error(err.detail || `Failed to update Department`);
    }
    return res.json();
}

export async function deleteDepartment(id: number): Promise<void> {
    const res = await fetch(`${BASE_URL}/departments/${id}`, {
        method: 'DELETE',
    });
    if (!res.ok) throw new Error(`Failed to delete Department: ${res.status}`);
}

// ==========================================
// Course API
// ==========================================
export async function fetchCourses(): Promise<any[]> {
    const res = await fetch(`${BASE_URL}/courses`);
    if (!res.ok) throw new Error(`Failed to fetch courses: ${res.status}`);
    return res.json();
}

export async function fetchCourse(id: number): Promise<any> {
    const res = await fetch(`${BASE_URL}/courses/${id}`);
    if (!res.ok) throw new Error(`Failed to fetch Course: ${res.status}`);
    return res.json();
}

export async function createCourse(data: any): Promise<any> {
    const res = await fetch(`${BASE_URL}/courses`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
    });
    if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: `HTTP ${res.status}` }));
        throw new Error(err.detail || `Failed to create Course`);
    }
    return res.json();
}

export async function updateCourse(id: number, data: any): Promise<any> {
    const res = await fetch(`${BASE_URL}/courses/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
    });
    if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: `HTTP ${res.status}` }));
        throw new Error(err.detail || `Failed to update Course`);
    }
    return res.json();
}

export async function deleteCourse(id: number): Promise<void> {
    const res = await fetch(`${BASE_URL}/courses/${id}`, {
        method: 'DELETE',
    });
    if (!res.ok) throw new Error(`Failed to delete Course: ${res.status}`);
}

// ==========================================
// Enrollment API
// ==========================================
export async function fetchEnrollments(): Promise<any[]> {
    const res = await fetch(`${BASE_URL}/enrollments`);
    if (!res.ok) throw new Error(`Failed to fetch enrollments: ${res.status}`);
    return res.json();
}

export async function fetchEnrollment(id: number): Promise<any> {
    const res = await fetch(`${BASE_URL}/enrollments/${id}`);
    if (!res.ok) throw new Error(`Failed to fetch Enrollment: ${res.status}`);
    return res.json();
}

export async function createEnrollment(data: any): Promise<any> {
    const res = await fetch(`${BASE_URL}/enrollments`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
    });
    if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: `HTTP ${res.status}` }));
        throw new Error(err.detail || `Failed to create Enrollment`);
    }
    return res.json();
}

export async function updateEnrollment(id: number, data: any): Promise<any> {
    const res = await fetch(`${BASE_URL}/enrollments/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
    });
    if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: `HTTP ${res.status}` }));
        throw new Error(err.detail || `Failed to update Enrollment`);
    }
    return res.json();
}

export async function deleteEnrollment(id: number): Promise<void> {
    const res = await fetch(`${BASE_URL}/enrollments/${id}`, {
        method: 'DELETE',
    });
    if (!res.ok) throw new Error(`Failed to delete Enrollment: ${res.status}`);
}

// ==========================================
// Grade API
// ==========================================
export async function fetchGrades(): Promise<any[]> {
    const res = await fetch(`${BASE_URL}/grades`);
    if (!res.ok) throw new Error(`Failed to fetch grades: ${res.status}`);
    return res.json();
}

export async function fetchGrade(id: number): Promise<any> {
    const res = await fetch(`${BASE_URL}/grades/${id}`);
    if (!res.ok) throw new Error(`Failed to fetch Grade: ${res.status}`);
    return res.json();
}

export async function createGrade(data: any): Promise<any> {
    const res = await fetch(`${BASE_URL}/grades`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
    });
    if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: `HTTP ${res.status}` }));
        throw new Error(err.detail || `Failed to create Grade`);
    }
    return res.json();
}

export async function updateGrade(id: number, data: any): Promise<any> {
    const res = await fetch(`${BASE_URL}/grades/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
    });
    if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: `HTTP ${res.status}` }));
        throw new Error(err.detail || `Failed to update Grade`);
    }
    return res.json();
}

export async function deleteGrade(id: number): Promise<void> {
    const res = await fetch(`${BASE_URL}/grades/${id}`, {
        method: 'DELETE',
    });
    if (!res.ok) throw new Error(`Failed to delete Grade: ${res.status}`);
}

// ==========================================
// Assignment API
// ==========================================
export async function fetchAssignments(): Promise<any[]> {
    const res = await fetch(`${BASE_URL}/assignments`);
    if (!res.ok) throw new Error(`Failed to fetch assignments: ${res.status}`);
    return res.json();
}

export async function fetchAssignment(id: number): Promise<any> {
    const res = await fetch(`${BASE_URL}/assignments/${id}`);
    if (!res.ok) throw new Error(`Failed to fetch Assignment: ${res.status}`);
    return res.json();
}

export async function createAssignment(data: any): Promise<any> {
    const res = await fetch(`${BASE_URL}/assignments`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
    });
    if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: `HTTP ${res.status}` }));
        throw new Error(err.detail || `Failed to create Assignment`);
    }
    return res.json();
}

export async function updateAssignment(id: number, data: any): Promise<any> {
    const res = await fetch(`${BASE_URL}/assignments/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
    });
    if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: `HTTP ${res.status}` }));
        throw new Error(err.detail || `Failed to update Assignment`);
    }
    return res.json();
}

export async function deleteAssignment(id: number): Promise<void> {
    const res = await fetch(`${BASE_URL}/assignments/${id}`, {
        method: 'DELETE',
    });
    if (!res.ok) throw new Error(`Failed to delete Assignment: ${res.status}`);
}

