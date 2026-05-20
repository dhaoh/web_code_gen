import React, { useState, useEffect } from 'react';

interface StudentItem {
    id: number;
    name: string;
    email: string;
}

interface StudentListPageProps {
    apiBaseUrl: string;
}

export default function StudentListPage({ apiBaseUrl }: StudentListPageProps) {
    const [items, setItems] = useState<StudentItem[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const fetchItems = async () => {
        try {
            const res = await fetch(`${apiBaseUrl}/students`);
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            const data = await res.json();
            setItems(data);
            setLoading(false);
        } catch (e: any) {
            setError(e.message);
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchItems();
    }, []);

    const handleDelete = async (id: number) => {
        if (!confirm('Delete this Student?')) return;
        try {
            await fetch(`${apiBaseUrl}/students/${id}`, { method: 'DELETE' });
            setItems(items.filter(i => i.id !== id));
        } catch (e: any) {
            alert('Failed to delete: ' + e.message);
        }
    };

    if (loading) return <div className="p-4">Loading...</div>;
    if (error) return <div className="p-4 text-red-500">Error: {error}</div>;

    return (
        <div className="p-4">
            <div className="flex justify-between items-center mb-4">
                <h1 className="text-2xl font-bold">Students</h1>
                <a
                    href={`/students/new`}
                    className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
                >
                    Create New
                </a>
            </div>

            <table className="w-full border-collapse border border-gray-300">
                <thead>
                    <tr className="bg-gray-100">
                        <th className="border p-2 text-left">Id</th>
                        <th className="border p-2 text-left">Name</th>
                        <th className="border p-2 text-left">Email</th>
                        <th className="border p-2 text-left">Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {items.map(item => (
                        <tr key={item.id} className="hover:bg-gray-50">
                            <td className="border p-2">{String(item.id)}</td>
                            <td className="border p-2">{String(item.name)}</td>
                            <td className="border p-2">{String(item.email)}</td>
                            <td className="border p-2">
                                <a
                                    href={`/students/${item.id}/edit`}
                                    className="text-blue-500 mr-3 hover:underline"
                                >
                                    Edit
                                </a>
                                <button
                                    onClick={() => handleDelete(item.id)}
                                    className="text-red-500 hover:underline"
                                >
                                    Delete
                                </button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}