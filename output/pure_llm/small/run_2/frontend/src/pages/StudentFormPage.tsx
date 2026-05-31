import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { createStudent, updateStudent, fetchStudent, Student } from '../api';

export default function StudentFormPage() {
  const { id } = useParams();
  const isEdit = !!id;
  const navigate = useNavigate();
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (isEdit) {
      fetchStudent(Number(id))
        .then(s => { setName(s.name); setEmail(s.email); })
        .catch(err => setError(err.message));
    }
  }, [id]);

  const validate = (): boolean => {
    if (!name.trim() || !email.trim()) {
      setError('Name and email are required');
      return false;
    }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      setError('Invalid email format');
      return false;
    }
    return true;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    if (!validate()) return;
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
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>{isEdit ? 'Edit Student' : 'Add Student'}</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <form onSubmit={handleSubmit}>
        <div>
          <label>Name: </label>
          <input value={name} onChange={e => setName(e.target.value)} required />
        </div>
        <div style={{ marginTop: '0.5rem' }}>
          <label>Email: </label>
          <input value={email} onChange={e => setEmail(e.target.value)} required type="email" />
        </div>
        <div style={{ marginTop: '1rem' }}>
          <button type="submit" disabled={loading}>
            {loading ? 'Saving...' : 'Save'}
          </button>
          <button type="button" onClick={() => navigate('/students')} style={{ marginLeft: '0.5rem' }}>
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
}