import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { StudentCreate, getStudent, createStudent, updateStudent } from '../api';

const StudentFormPage: React.FC = () => {
  const { id } = useParams();
  const isEdit = Boolean(id);
  const navigate = useNavigate();

  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (isEdit) {
      const fetchStudent = async () => {
        try {
          setLoading(true);
          const student = await getStudent(Number(id));
          setName(student.name);
          setEmail(student.email);
        } catch (err: any) {
          setError(err.message);
        } finally {
          setLoading(false);
        }
      };
      fetchStudent();
    }
  }, [id, isEdit]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim()) {
      alert('Name is required');
      return;
    }
    if (!email.trim()) {
      alert('Email is required');
      return;
    }
    const data: StudentCreate = { name: name.trim(), email: email.trim() };
    try {
      setLoading(true);
      if (isEdit) {
        await updateStudent(Number(id), data);
      } else {
        await createStudent(data);
      }
      navigate('/students');
    } catch (err: any) {
      setError(err.message);
      setLoading(false);
    }
  };

  if (loading && isEdit) return <p>Loading...</p>;
  if (error) return <p style={{ color: 'red' }}>Error: {error}</p>;

  return (
    <div>
      <h2>{isEdit ? 'Edit Student' : 'Add Student'}</h2>
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
        <div style={{ marginTop: 8 }}>
          <label>Email:</label>
          <input
            type="email"
            value={email}
            onChange={e => setEmail(e.target.value)}
            required
          />
        </div>
        <div style={{ marginTop: 16 }}>
          <button type="submit" disabled={loading}>
            {loading ? 'Saving...' : 'Save'}
          </button>
          <button type="button" onClick={() => navigate('/students')} style={{ marginLeft: 8 }}>
            Cancel
          </button>
        </div>
        {error && <p style={{ color: 'red' }}>{error}</p>}
      </form>
    </div>
  );
};

export default StudentFormPage;