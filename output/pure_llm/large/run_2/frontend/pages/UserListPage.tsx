import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { list, remove } from '../api';

const UserListPage: React.FC = () => {
  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const load = async () => {
    try {
      const res = await list('users');
      setData(res);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };
  useEffect(() => { load(); }, []);

  const handleDelete = async (id: number) => {
    if (!window.confirm('Delete?')) return;
    try {
      await remove('users', id);
      setData(prev => prev.filter(u => u.id !== id));
    } catch (err: any) {
      alert(err.message);
    }
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  if (data.length === 0) return <div>No users found.</div>;

  return (
    <div>
      <h2>Users</h2>
      <Link to="/users/new">Create New</Link>
      <table>
        <thead><tr><th>ID</th><th>Username</th><th>Role</th><th>Full Name</th><th>Email</th><th/> </tr></thead>
        <tbody>
          {data.map(u => (
            <tr key={u.id}>
              <td>{u.id}</td>
              <td>{u.username}</td>
              <td>{u.role}</td>
              <td>{u.full_name}</td>
              <td>{u.email}</td>
              <td>
                <Link to={`/users/${u.id}/edit`}>Edit</Link>
                <button onClick={() => handleDelete(u.id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default UserListPage;