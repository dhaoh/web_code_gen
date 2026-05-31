import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../api';

interface Department {
  id: number;
  name: string;
  code: string;
}

export default function DepartmentListPage() {
  const [items, setItems] = useState<Department[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const fetchAll = async () => {
    try {
      setLoading(true);
      setItems(await api.getDepartments());
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchAll(); }, []);

  const handleDelete = async (id: number) => {
    if (!confirm('Delete?')) return;
    try {
      await api.deleteDepartment(id);
      setItems(prev => prev.filter(i => i.id !== id));
    } catch (err: any) { alert(err.message); }
  };

  if (loading) return <p>Loading...</p>;
  if (error) return <p style={{ color: 'red' }}>Error: {error}</p>;

  return (
    <div>
      <h2>Departments</h2>
      <Link to="/departments/new">Create New</Link>
      {items.length === 0 ? (
        <p>No departments.</p>
      ) : (
        <table border={1} cellPadding={5}>
          <thead><tr><th>ID</th><th>Name</th><th>Code</th><th>Actions</th></tr></thead>
          <tbody>
            {items.map(d => (
              <tr key={d.id}>
                <td>{d.id}</td><td>{d.name}</td><td>{d.code}</td>
                <td>
                  <Link to={`/departments/${d.id}/edit`}>Edit</Link>{' '}
                  <button onClick={() => handleDelete(d.id)}>Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}