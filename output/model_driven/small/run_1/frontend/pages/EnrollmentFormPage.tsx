import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';

interface EnrollmentFormData {
    student_id: number;
    course_id: number;
    enrolled_at: string;
}

export default function EnrollmentFormPage() {
    const { id } = useParams<{ id: string }>();
    const navigate = useNavigate();
    const isEdit = Boolean(id);

    const [formData, setFormData] = useState<EnrollmentFormData>({
        student_id: 0,
        course_id: 0,
        enrolled_at: '',
    });
    const [saving, setSaving] = useState(false);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        if (isEdit) {
            fetch(`http://localhost:8000/enrollments/${id}`)
                .then(res => res.json())
                .then(data => {
                    const fd: any = {};
                    fd.student_id = data.student_id;
                    fd.course_id = data.course_id;
                    fd.enrolled_at = data.enrolled_at;
                    setFormData(fd);
                })
                .catch(e => setError(e.message));
        }
    }, [id]);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
        let value: any = e.target.value;
        if (e.target.name === 'id') value = Number(value);
        if (e.target.name === 'student_id') value = Number(value);
        if (e.target.name === 'course_id') value = Number(value);
        setFormData({ ...formData, [e.target.name]: value });
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setSaving(true);
        setError(null);

        const url = isEdit
            ? `http://localhost:8000/enrollments/${id}`
            : `http://localhost:8000/enrollments`;

        try {
            const res = await fetch(url, {
                method: isEdit ? 'PUT' : 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData),
            });
            if (!res.ok) {
                const err = await res.json();
                throw new Error(err.detail || `HTTP ${res.status}`);
            }
            navigate('/enrollments');
        } catch (e: any) {
            setError(e.message);
            setSaving(false);
        }
    };

    return (
        <div className="max-w-lg mx-auto p-4">
            <h1 className="text-2xl font-bold mb-4">
                {isEdit ? 'Edit' : 'Create'} Enrollment
            </h1>

            {error && (
                <div className="bg-red-100 border border-red-400 text-red-700 p-3 rounded mb-4">
                    {error}
                </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                    <label className="block text-sm font-medium mb-1">
                        Student Id *                    </label>
                    <input
                        type="number"
                        name="student_id"
                        value={formData.student_id}
                        onChange={handleChange}
                        className="w-full border rounded p-2"
required                    />
                </div>
                <div>
                    <label className="block text-sm font-medium mb-1">
                        Course Id *                    </label>
                    <input
                        type="number"
                        name="course_id"
                        value={formData.course_id}
                        onChange={handleChange}
                        className="w-full border rounded p-2"
required                    />
                </div>
                <div>
                    <label className="block text-sm font-medium mb-1">
                        Enrolled At *                    </label>
                    <input
                        type="datetime-local"
                        name="enrolled_at"
                        value={formData.enrolled_at}
                        onChange={handleChange}
                        className="w-full border rounded p-2"
required                    />
                </div>

                <div className="flex gap-3">
                    <button
                        type="submit"
                        disabled={saving}
                        className="bg-blue-500 text-white px-6 py-2 rounded hover:bg-blue-600 disabled:opacity-50"
                    >
                        {saving ? 'Saving...' : 'Save'}
                    </button>
                    <button
                        type="button"
                        onClick={() => navigate('/enrollments')}
                        className="bg-gray-300 px-6 py-2 rounded hover:bg-gray-400"
                    >
                        Cancel
                    </button>
                </div>
            </form>
        </div>
    );
}
