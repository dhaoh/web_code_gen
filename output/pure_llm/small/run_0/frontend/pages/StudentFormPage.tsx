import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { createStudent, updateStudent, fetchStudent } from '../api';

const StudentFormPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const isEdit = Boolean(id);
  const navigate = useNavigate();

  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (isEdit && id) {
      setLoading(true);
      fetchStudent(Number(id))
        .then(student => {
          setName(student.name);
          setEmail(student.email);
        })
        .catch(err => setError(err.message))
        .finally(() => setLoading(false));
    }
  }, [id, isEdit]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    if (!name.trim() || !email.trim()) {
      setError('Name and email are required');
      return;
    }
    try {
      if (isEdit && id) {
        await updateStudent(Number(id), { name, email });
      } else {
        await createStudent({ name, email });
      }
      navigate('/students');
    } catch (err: any) {
      setError(err.message);
    }
  };

  if (loading) return <div>Loading...</div>;

  return (
    <div>
      <h2>{isEdit ? 'Edit Student' : 'Add Student'}</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <form onSubmit={handleSubmit}>
        <div>
          <label>Name: </label>
          <input value={name} onChange={e => setName(e.target.value)} required />
        </div>
        <div>
          <label>Email: </label>
          <input value={email} onChange={e => setEmail(e.target.value)} type="email" required />
        </div>
        <button type="submit">{isEdit ? 'Update' : 'Create'}</button>
        <button type="button" onClick={() => navigate('/students')} style={{ marginLeft: 8 }}>Cancel</button>
      </form>
    </div>
  );
};

export default StudentFormPage;