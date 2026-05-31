import { useState, useEffect, type ChangeEvent, type FormEvent } from 'react';
import { useParams, useNavigate } from 'react-router-dom';

interface PrerequisiteFormData {
    course_id: number;
    prerequisite_course_id: number;
    is_mandatory: boolean;
}

export default function PrerequisiteFormPage() {
    const { id } = useParams<{ id: string }>();
    const navigate = useNavigate();
    const isEdit = Boolean(id);

    const [formData, setFormData] = useState<PrerequisiteFormData>({
        course_id: 0,
        prerequisite_course_id: 0,
        is_mandatory: true,
    });
    const [saving, setSaving] = useState(false);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        if (isEdit) {
            fetch(`http://localhost:8000/prerequisites/${id}`)
                .then(res => {
                    if (!res.ok) throw new Error(`HTTP ${res.status}`);
                    return res.json();
                })
                .then(data => {
                    const fd: any = {};
                    fd.course_id = data.course_id ?? formData.course_id;
                    fd.prerequisite_course_id = data.prerequisite_course_id ?? formData.prerequisite_course_id;
                    fd.is_mandatory = data.is_mandatory ?? formData.is_mandatory;
                    setFormData(fd);
                })
                .catch(e => setError(e.message));
        }
    }, [id]);

    const handleChange = (e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
        let value: any = e.target.value;
        if (e.target.name === 'id') value = value === '' ? null : Number(value);
        if (e.target.name === 'course_id') value = value === '' ? null : Number(value);
        if (e.target.name === 'prerequisite_course_id') value = value === '' ? null : Number(value);
        if (e.target.name === 'is_mandatory') value = e.target.value === 'true';
        setFormData({ ...formData, [e.target.name]: value });
    };

    const handleSubmit = async (e: FormEvent) => {
        e.preventDefault();
        setSaving(true);
        setError(null);

        const url = isEdit
            ? `http://localhost:8000/prerequisites/${id}`
            : `http://localhost:8000/prerequisites`;

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
            navigate('/prerequisites');
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
                    onClick={() => navigate('/prerequisites')}
                    className="inline-flex items-center gap-1.5 text-sm text-slate-500 hover:text-slate-800 transition mb-3"
                >
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                    </svg>
                    Back to prerequisites
                </button>
                <h1 className="text-2xl font-bold text-slate-900">
                    {isEdit ? 'Edit' : 'Create New'} Prerequisite
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
                        <h2 className="text-sm font-semibold text-slate-700">Prerequisite Details</h2>
                    </div>
                    <div className="p-6 space-y-5">
                        <div>
                            <label className="block text-sm font-medium text-slate-700 mb-1.5">
                                Course Id
<span className="text-red-500 ml-0.5">*</span>                            </label>
                            <input
                                type="number"
                                name="course_id"
                                value={formData.course_id}
                                onChange={handleChange}
                                placeholder="Enter course id..."
                                className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition placeholder-slate-400"
                                required                            />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-slate-700 mb-1.5">
                                Prerequisite Course Id
<span className="text-red-500 ml-0.5">*</span>                            </label>
                            <input
                                type="number"
                                name="prerequisite_course_id"
                                value={formData.prerequisite_course_id}
                                onChange={handleChange}
                                placeholder="Enter prerequisite course id..."
                                className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition placeholder-slate-400"
                                required                            />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-slate-700 mb-1.5">
                                Is Mandatory
<span className="text-red-500 ml-0.5">*</span>                            </label>
                            <select
                                name="is_mandatory"
                                value={String(formData.is_mandatory)}
                                onChange={handleChange}
                                className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent bg-white transition"
                            >
                                <option value="true">Yes</option>
                                <option value="false">No</option>
                            </select>
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
                                    {isEdit ? 'Save Changes' : 'Create Prerequisite'}
                                </>
                            )}
                        </button>
                        <button
                            type="button"
                            onClick={() => navigate('/prerequisites')}
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
