import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getOne, create, update } from '../api';

const UserFormPage: React.FC = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const isEdit = !!id;
  const [form, setForm] = useState({ username: '', password: '', role: 'student', full_name: '', email: '', major_id: '' });
  const [error, setError] = useState('');

  useEffect(() => {
    if (isEdit) {
      getOne('users', Number(id)).then(data => {
        setForm({ username: data.username, password: '', role: data.role, full_name: data.full_name, email: data.email, major_id: data.major_id || '' });
      });
    }
  }, [id]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const payload = { ...form, major_id: form.major_id ? Number(form.major_id) : null };
    try {
      if (isEdit) {
        await update('users', Number(id), payload);
      } else {
        await create('users', payload);
      }
      navigate('/users');
    } catch (err: any) {
      setError(err.message);
    }
  };

  return (
    <div>
      <h2>{isEdit ? 'Edit' : 'Create'} User</h2>
      <form onSubmit={handleSubmit}>
        <label>Username: <input name="username" value={form.username} onChange={handleChange} required /></label><br/>
        <label>Password: <input name="password" type="password" value={form.password} onChange={handleChange} required={!isEdit} /></label><br/>
        <label>Role: <select name="role" value={form.role} onChange={handleChange}>
          <option value="student">Student</option>
          <option value="teacher">Teacher</option>
          <option value="admin">Admin</option>
          <option value="department_head">Department Head</option>
        </select></label><br/>
        <label>Full Name: <input name="full_name" value={form.full_name} onChange={handleChange} required /></label><br/>
        <label>Email: <input name="email" value={form.email} type="email" onChange={handleChange} required /></label><br/>
        <label>Major ID: <input name="major_id" type="number" value={form.major_id} onChange={handleChange} /></label><br/>
        <button type="submit">Save</button>
        {error && <p style={{ color: 'red' }}>{error}</p>}
      </form>
    </div>
  );
};

export default UserFormPage;