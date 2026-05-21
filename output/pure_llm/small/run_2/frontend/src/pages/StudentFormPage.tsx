import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { getStudent, createStudent, updateStudent } from '../api';

export default function StudentFormPage() {
  const { id } = useParams<{ id?: string }>();
  const isEdit = Boolean(id);
  const navigate = useNavigate();

  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (isEdit) {
      setLoading(true);
      getStudent(Number(id))
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
    setLoading(true);
    try {
      if (isEdit) {
        await updateStudent(Number(id), { name, email });
      } else {
        await createStudent({ name, email });
      }
      navigate('/students');
    } catch (err: any) {
      setError(err.message);
      setLoading(false);
    }
  };

  if (isEdit && loading) return <div>Loading student data...</div>;

  return (
    <div>
      <h2>{isEdit ? 'Edit Student' : 'Add Student'}</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <form onSubmit={handleSubmit}>
        <div>
          <label>Name:</label>
          <input
            type="text"
            value={name}
            onChange={e => setName(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Email:</label>
          <input
            type="email"
            value={email}
            onChange={e => setEmail(e.target.value)}
            required
          />
        </div>
        <button type="submit" disabled={loading}>{isEdit ? 'Update' : 'Create'}</button>
        <button type="button" onClick={() => navigate('/students')}>Cancel</button>
      </form>
    </div>
  );
}