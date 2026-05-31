import { useState, useEffect } from 'react';

interface CourseScheduleItem {
    id: number;
    course_id: number;
    schedule_id: number;
}

interface CourseScheduleListPageProps {
    apiBaseUrl: string;
}

export default function CourseScheduleListPage({ apiBaseUrl }: CourseScheduleListPageProps) {
    const [items, setItems] = useState<CourseScheduleItem[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [search, setSearch] = useState('');

    const fetchItems = async () => {
        setLoading(true);
        setError(null);
        try {
            const res = await fetch(`${apiBaseUrl}/courseschedules`);
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            const data = await res.json();
            setItems(data);
        } catch (e: any) {
            setError(e.message);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => { fetchItems(); }, []);

    const handleDelete = async (id: number) => {
        if (!confirm('Permanently delete this courseschedule?')) return;
        try {
            const res = await fetch(`${apiBaseUrl}/courseschedules/${id}`, { method: 'DELETE' });
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            setItems(items.filter(i => i.id !== id));
        } catch (e: any) {
            alert('Delete failed: ' + e.message);
        }
    };

    const filtered = items.filter(item =>
        Object.values(item).some(v =>
            String(v).toLowerCase().includes(search.toLowerCase())
        )
    );

    return (
        <div className="p-6 max-w-7xl">
            {/* Header */}
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
                <div>
                    <h1 className="text-2xl font-bold text-slate-900">Courseschedules</h1>
                    <p className="text-sm text-slate-500 mt-0.5">
                        {filtered.length} of {items.length} record{items.length !== 1 ? 's' : ''}
                    </p>
                </div>
                <a
                    href={`/courseschedules/new`}
                    className="inline-flex items-center gap-2 bg-indigo-600 text-white px-4 py-2.5 rounded-lg text-sm font-medium hover:bg-indigo-700 transition shadow-sm"
                >
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                    </svg>
                    Add Courseschedule
                </a>
            </div>

            {/* Search */}
            <div className="mb-4">
                <div className="relative max-w-sm">
                    <svg className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                    </svg>
                    <input
                        type="text"
                        placeholder="Search..."
                        value={search}
                        onChange={e => setSearch(e.target.value)}
                        className="w-full pl-10 pr-4 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent bg-white"
                    />
                </div>
            </div>

            {/* States */}
            {loading && (
                <div className="bg-white rounded-xl border border-slate-200 p-12 text-center">
                    <div className="inline-block w-8 h-8 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin mb-3"></div>
                    <p className="text-slate-500 text-sm">Loading courseschedules...</p>
                </div>
            )}

            {error && (
                <div className="bg-red-50 border border-red-200 rounded-xl p-4 flex items-center gap-3">
                    <span className="text-red-500 text-lg">⚠️</span>
                    <div>
                        <p className="text-red-800 text-sm font-medium">Failed to load data</p>
                        <p className="text-red-600 text-xs mt-0.5">{error}</p>
                    </div>
                    <button onClick={fetchItems} className="ml-auto text-sm text-red-600 hover:text-red-800 font-medium">
                        Retry
                    </button>
                </div>
            )}

            {!loading && !error && filtered.length === 0 && (
                <div className="bg-white rounded-xl border border-slate-200 p-12 text-center">
                    <span className="text-4xl block mb-3">
                        {search ? '🔍' : '📭'}
                    </span>
                    <p className="text-slate-600 font-medium">
                        {search ? 'No matching records found' : 'No courseschedules yet'}
                    </p>
                    <p className="text-slate-400 text-sm mt-1">
                        {search ? 'Try a different search term' : 'Create your first courseschedule to get started'}
                    </p>
                    {!search && (
                        <a href={`/courseschedules/new`} className="inline-block mt-4 text-sm text-indigo-600 hover:text-indigo-800 font-medium">
                            + Add Courseschedule
                        </a>
                    )}
                </div>
            )}

            {/* Table */}
            {!loading && !error && filtered.length > 0 && (
                <div className="bg-white rounded-xl border border-slate-200 overflow-hidden shadow-sm">
                    <div className="overflow-x-auto">
                        <table className="w-full">
                            <thead>
                                <tr className="bg-slate-50 border-b border-slate-200">
                                    <th className="text-left px-5 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wider">
                                        Id
                                    </th>
                                    <th className="text-left px-5 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wider">
                                        Course Id
                                    </th>
                                    <th className="text-left px-5 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wider">
                                        Schedule Id
                                    </th>
                                    <th className="text-right px-5 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wider w-24">
                                        Actions
                                    </th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-slate-100">
                                {filtered.map((item, idx) => (
                                    <tr key={item.id} className={`hover:bg-slate-50 transition ${idx % 2 === 0 ? 'bg-white' : 'bg-slate-50/30'}`}>
                                        <td className="px-5 py-3 text-sm font-mono text-slate-400">#{String(item.id)}</td>
                                        <td className="px-5 py-3 text-sm text-slate-700">
                                            {item.course_id != null ? String(item.course_id) : <span className="text-slate-300">—</span>}
                                        </td>
                                        <td className="px-5 py-3 text-sm text-slate-700">
                                            {item.schedule_id != null ? String(item.schedule_id) : <span className="text-slate-300">—</span>}
                                        </td>
                                        <td className="px-5 py-3 text-right">
                                            <div className="flex items-center justify-end gap-1">
                                                <a
                                                    href={`/courseschedules/${item.id}/edit`}
                                                    className="p-1.5 text-slate-400 hover:text-indigo-600 hover:bg-indigo-50 rounded-lg transition"
                                                    title="Edit"
                                                >
                                                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                                                    </svg>
                                                </a>
                                                <button
                                                    onClick={() => handleDelete(item.id)}
                                                    className="p-1.5 text-slate-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition"
                                                    title="Delete"
                                                >
                                                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                                                    </svg>
                                                </button>
                                            </div>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>
            )}
        </div>
    );
}
