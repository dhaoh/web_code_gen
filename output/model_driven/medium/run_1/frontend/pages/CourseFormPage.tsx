import { useState, useEffect, type ChangeEvent, type FormEvent } from 'react';
import { useParams, useNavigate } from 'react-router-dom';

interface CourseFormData {
    title: string;
    description: string;
    capacity: number;
    credits: number;
    department_id: number;
}

export default function CourseFormPage() {
    const { id } = useParams<{ id: string }>();
    const navigate = useNavigate();
    const isEdit = Boolean(id);

    const [formData, setFormData] = useState<CourseFormData>({
        title: '',
        description: '',
        capacity: 30,
        credits: 3,
        department_id: 0,
    });
    const [saving, setSaving] = useState(false);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        if (isEdit) {
            fetch(`http://localhost:8000/courses/${id}`)
                .then(res => {
                    if (!res.ok) throw new Error(`HTTP ${res.status}`);
                    return res.json();
                })
                .then(data => {
                    const fd: any = {};
                    fd.title = data.title ?? formData.title;
                    fd.description = data.description ?? formData.description;
                    fd.capacity = data.capacity ?? formData.capacity;
                    fd.credits = data.credits ?? formData.credits;
                    fd.department_id = data.department_id ?? formData.department_id;
                    setFormData(fd);
                })
                .catch(e => setError(e.message));
        }
    }, [id]);

    const handleChange = (e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
        let value: any = e.target.value;
        if (e.target.name === 'id') value = value === '' ? null : Number(value);
        if (e.target.name === 'capacity') value = value === '' ? null : Number(value);
        if (e.target.name === 'credits') value = value === '' ? null : Number(value);
        if (e.target.name === 'department_id') value = value === '' ? null : Number(value);
        setFormData({ ...formData, [e.target.name]: value });
    };

    const handleSubmit = async (e: FormEvent) => {
        e.preventDefault();
        setSaving(true);
        setError(null);

        const url = isEdit
            ? `http://localhost:8000/courses/${id}`
            : `http://localhost:8000/courses`;

        try {
            const res = await fetch(url, {
                method: isEdit ? 'PUT' : 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData),
            });
            if (!res.ok) {
                const err = await res.json().catch(() => ({ detail: `HTTP ${res.status}` }));
                throw new Error(err.detail || `Request failed with status ${res.status}`);
            }
            navigate('/courses');
        } catch (e: any) {
            setError(e.message);
            setSaving(false);
        }
    };

    return (
        <div className="p-6 max-w-2xl">
            {/* Header */}
            <div className="mb-6">
                <button
                    onClick={() => navigate('/courses')}
                    className="inline-flex items-center gap-1.5 text-sm text-slate-500 hover:text-slate-800 transition mb-3"
                >
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                    </svg>
                    Back to courses
                </button>
                <h1 className="text-2xl font-bold text-slate-900">
                    {isEdit ? 'Edit' : 'Create New'} Course
                </h1>
                <p className="text-sm text-slate-500 mt-1">
                    {isEdit ? 'Update the fields below' : 'Fill in the details below to create a new record'}
                </p>
            </div>

            {/* Error */}
            {error && (
                <div className="bg-red-50 border border-red-200 rounded-xl p-4 flex items-start gap-3 mb-6">
                    <span className="text-red-500 text-lg shrink-0">⚠️</span>
                    <div className="flex-1">
                        <p className="text-red-800 text-sm font-medium">An error occurred</p>
                        <p className="text-red-600 text-xs mt-0.5">{error}</p>
                    </div>
                    <button onClick={() => setError(null)} className="text-red-400 hover:text-red-600">
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>
                </div>
            )}

            {/* Form */}
            <form onSubmit={handleSubmit}>
                <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
                    <div className="px-6 py-4 border-b border-slate-100 bg-slate-50/50">
                        <h2 className="text-sm font-semibold text-slate-700">Course Details</h2>
                    </div>
                    <div className="p-6 space-y-5">
                        <div>
                            <label className="block text-sm font-medium text-slate-700 mb-1.5">
                                Title
<span className="text-red-500 ml-0.5">*</span>                            </label>
                            <textarea
                                name="title"
                                value={formData.title}
                                onChange={handleChange}
                                rows={3}
                                placeholder="Enter title..."
                                className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition placeholder-slate-400"
required                            />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-slate-700 mb-1.5">
                                Description
                            </label>
                            <input
                                type="text"
                                name="description"
                                value={formData.description}
                                onChange={handleChange}
                                placeholder="Enter description..."
                                className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition placeholder-slate-400"
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-slate-700 mb-1.5">
                                Capacity
<span className="text-red-500 ml-0.5">*</span>                            </label>
                            <input
                                type="number"
                                name="capacity"
                                value={formData.capacity}
                                onChange={handleChange}
                                placeholder="Enter capacity..."
                                className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition placeholder-slate-400"
                                required                            />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-slate-700 mb-1.5">
                                Credits
<span className="text-red-500 ml-0.5">*</span>                            </label>
                            <input
                                type="number"
                                name="credits"
                                value={formData.credits}
                                onChange={handleChange}
                                placeholder="Enter credits..."
                                className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition placeholder-slate-400"
                                required                            />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-slate-700 mb-1.5">
                                Department Id
<span className="text-red-500 ml-0.5">*</span>                            </label>
                            <input
                                type="number"
                                name="department_id"
                                value={formData.department_id}
                                onChange={handleChange}
                                placeholder="Enter department id..."
                                className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition placeholder-slate-400"
                                required                            />
                        </div>
                    </div>

                    {/* Actions */}
                    <div className="px-6 py-4 border-t border-slate-100 bg-slate-50/50 flex items-center gap-3">
                        <button
                            type="submit"
                            disabled={saving}
                            className="inline-flex items-center gap-2 bg-indigo-600 text-white px-5 py-2.5 rounded-lg text-sm font-medium hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition shadow-sm"
                        >
                            {saving ? (
                                <>
                                    <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                                    Saving...
                                </>
                            ) : (
                                <>
                                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                                    </svg>
                                    {isEdit ? 'Save Changes' : 'Create Course'}
                                </>
                            )}
                        </button>
                        <button
                            type="button"
                            onClick={() => navigate('/courses')}
                            className="px-5 py-2.5 rounded-lg text-sm font-medium text-slate-600 hover:text-slate-800 hover:bg-slate-200 transition"
                        >
                            Cancel
                        </button>
                    </div>
                </div>
            </form>
        </div>
    );
}
