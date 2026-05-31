import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { apiListDepartments, apiDeleteDepartment } from '../../api';

export default function DepartmentList() {
  const [departments, setDepartments] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    apiListDepartments().then(setDepartments).catch(err => setError(err.message)).finally(() => setLoading(false));
  }, []);

  const handleDelete = async (id: number) => {
    if (!window.confirm('Delete?')) return;
    try {
      await apiDeleteDepartment(id);
      setDepartments(deps => deps.filter(d => d.id !== id));
    } catch (err: any) {
      alert(err.message);
    }
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div className="alert alert-danger">{error}</div>;

  return (
    <div>
      <h2>Departments</h2>
      <Link to="/departments/new" className="btn btn-primary mb-3">Create Department</Link>
      {departments.length === 0 ? (
        <p>No departments found.</p>
      ) : (
        <table className="table">
          <thead><tr><th>ID</th><th>Name</th><th>Code</th><th>Actions</th></tr></thead>
          <tbody>
            {departments.map(d => (
              <tr key={d.id}>
                <td>{d.id}</td>
                <td>{d.name}</td>
                <td>{d.code}</td>
                <td>
                  <Link to={`/departments/${d.id}/edit`} className="btn btn-sm btn-outline-secondary me-1">Edit</Link>
                  <button className="btn btn-sm btn-outline-danger" onClick={() => handleDelete(d.id)}>Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}