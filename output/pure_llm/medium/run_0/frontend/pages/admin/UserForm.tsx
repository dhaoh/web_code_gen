import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { apiCreateUser, apiUpdateUser, apiListUsers } from '../../api';

export default function UserForm() {
  const { id } = useParams<{ id: string }>();
  const isEdit = Boolean(id);
  const navigate = useNavigate();

  const [form, setForm] = useState({
    username: '',
    password: '',
    role: 'student',
    full_name: '',
    email: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (isEdit) {
      const fetchUser = async () => {
        try {
          const users = await apiListUsers(); // quick fetch, but better would be dedicated endpoint
          const user = users.find((u: any) => u.id === Number(id));
          if (user) {
            setForm({
              username: user.username,
              password: '',
              role: user.role,
              full_name: user.full_name,
              email: user.email
            });
          }
        } catch (err: any) {
          setError(err.message);
        }
      };
      fetchUser();
    }
  }, [id, isEdit]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      if (isEdit) {
        const payload = { ...form };
        if (!payload.password) delete (payload as any).password; // don't send empty password
        await apiUpdateUser(Number(id), payload);
      } else {
        await apiCreateUser(form);
      }
      navigate('/users');
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>{isEdit ? 'Edit User' : 'Create User'}</h2>
      {error && <div className="alert alert-danger">{error}</div>}
      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label>Username</label>
          <input className="form-control" name="username" value={form.username} onChange={handleChange} required />
        </div>
        <div className="mb-3">
          <label>Password {isEdit && '(leave blank to keep unchanged)'}</label>
          <input type="password" className="form-control" name="password" value={form.password} onChange={handleChange} required={!isEdit} />
        </div>
        <div className="mb-3">
          <label>Role</label>
          <select className="form-select" name="role" value={form.role} onChange={handleChange}>
            <option value="student">Student</option>
            <option value="teacher">Teacher</option>
            <option value="admin">Admin</option>
          </select>
        </div>
        <div className="mb-3">
          <label>Full Name</label>
          <input className="form-control" name="full_name" value={form.full_name} onChange={handleChange} required />
        </div>
        <div className="mb-3">
          <label>Email</label>
          <input type="email" className="form-control" name="email" value={form.email} onChange={handleChange} required />
        </div>
        <button type="submit" className="btn btn-primary" disabled={loading}>
          {loading ? 'Saving...' : 'Save'}
        </button>
        <button type="button" className="btn btn-secondary ms-2" onClick={() => navigate('/users')}>Cancel</button>
      </form>
    </div>
  );
}