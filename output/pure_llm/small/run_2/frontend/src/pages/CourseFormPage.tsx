import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { getCourse, createCourse, updateCourse } from '../api';

export default function CourseFormPage() {
  const { id } = useParams<{ id?: string }>();
  const isEdit = Boolean(id);
  const navigate = useNavigate();

  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [capacity, setCapacity] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (isEdit) {
      setLoading(true);
      getCourse(Number(id))
        .then(course => {
          setTitle(course.title);
          setDescription(course.description || '');
          setCapacity(course.capacity);
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
      const payload = { title, description: description || undefined, capacity };
      if (isEdit) {
        await updateCourse(Number(id), payload);
      } else {
        await createCourse(payload);
      }
      navigate('/courses');
    } catch (err: any) {
      setError(err.message);
      setLoading(false);
    }
  };

  if (isEdit && loading) return <div>Loading course data...</div>;

  return (
    <div>
      <h2>{isEdit ? 'Edit Course' : 'Add Course'}</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <form onSubmit={handleSubmit}>
        <div>
          <label>Title:</label>
          <input
            type="text"
            value={title}
            onChange={e => setTitle(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Description:</label>
          <textarea value={description} onChange={e => setDescription(e.target.value)} />
        </div>
        <div>
          <label>Capacity (minimum 1):</label>
          <input
            type="number"
            min={1}
            value={capacity}
            onChange={e => setCapacity(Math.max(1, parseInt(e.target.value) || 1))}
            required
          />
        </div>
        <button type="submit" disabled={loading}>{isEdit ? 'Update' : 'Create'}</button>
        <button type="button" onClick={() => navigate('/courses')}>Cancel</button>
      </form>
    </div>
  );
}