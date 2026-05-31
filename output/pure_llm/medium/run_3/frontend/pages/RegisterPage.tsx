import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../api';

const RegisterPage: React.FC = () => {
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [role, setRole] = useState('student');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      await api.register({ username, password, full_name: fullName, email, role });
      navigate('/login');
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>Register</h2>
      <form onSubmit={handleSubmit}>
        <div><label>Username:</label><input value={username} onChange={e => setUsername(e.target.value)} required /></div>
        <div><label>Password:</label><input type="password" value={password} onChange={e => setPassword(e.target.value)} required /></div>
        <div><label>Full Name:</label><input value={fullName} onChange={e => setFullName(e.target.value)} required /></div>
        <div><label>Email:</label><input type="email" value={email} onChange={e => setEmail(e.target.value)} required /></div>
        <div>
          <label>Role:</label>
          <select value={role} onChange={e => setRole(e.target.value)}>
            <option value="student">Student</option>
            <option value="teacher">Teacher</option>
          </select>
        </div>
        {error && <p style={{ color: 'red' }}>{error}</p>}
        <button type="submit" disabled={loading}>{loading ? 'Registering...' : 'Register'}</button>
      </form>
    </div>
  );
};

export default RegisterPage;