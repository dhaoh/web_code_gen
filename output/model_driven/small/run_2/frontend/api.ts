// Auto-generated API client for student_course_system_small

const BASE_URL = 'http://localhost:8000';

// ==========================================
// Student API
// ==========================================
export async function fetchStudents(): Promise<any[]> {
    const res = await fetch(`${BASE_URL}/students`);
    if (!res.ok) throw new Error(`Failed to fetch students: ${res.status}`);
    return res.json();
}

export async function fetchStudent(id: number): Promise<any> {
    const res = await fetch(`${BASE_URL}/students/${id}`);
    if (!res.ok) throw new Error(`Failed to fetch Student: ${res.status}`);
    return res.json();
}

export async function createStudent(data: any): Promise<any> {
    const res = await fetch(`${BASE_URL}/students`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
    });
    if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: `HTTP ${res.status}` }));
        throw new Error(err.detail || `Failed to create Student`);
    }
    return res.json();
}

export async function updateStudent(id: number, data: any): Promise<any> {
    const res = await fetch(`${BASE_URL}/students/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
    });
    if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: `HTTP ${res.status}` }));
        throw new Error(err.detail || `Failed to update Student`);
    }
    return res.json();
}

export async function deleteStudent(id: number): Promise<void> {
    const res = await fetch(`${BASE_URL}/students/${id}`, {
        method: 'DELETE',
    });
    if (!res.ok) throw new Error(`Failed to delete Student: ${res.status}`);
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

