import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { createCourse, updateCourse, fetchCourse } from '../api';

const CourseFormPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const isEdit = Boolean(id);
  const navigate = useNavigate();

  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [capacity, setCapacity] = useState<number>(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (isEdit && id) {
      setLoading(true);
      fetchCourse(Number(id))
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
    if (!title.trim() || capacity < 1) {
      setError('Title is required and capacity must be at least 1');
      return;
    }
    try {
      const payload = {
        title,
        description: description || undefined,
        capacity
      };
      if (isEdit && id) {
        await updateCourse(Number(id), payload);
      } else {
        await createCourse(payload);
      }
      navigate('/courses');
    } catch (err: any) {
      setError(err.message);
    }
  };

  if (loading) return <div>Loading...</div>;

  return (
    <div>
      <h2>{isEdit ? 'Edit Course' : 'Add Course'}</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <form onSubmit={handleSubmit}>
        <div>
          <label>Title: </label>
          <input value={title} onChange={e => setTitle(e.target.value)} required />
        </div>
        <div>
          <label>Description: </label>
          <textarea value={description} onChange={e => setDescription(e.target.value)} rows={3} />
        </div>
        <div>
          <label>Capacity: </label>
          <input type="number" min={1} value={capacity} onChange={e => setCapacity(Number(e.target.value))} required />
        </div>
        <button type="submit">{isEdit ? 'Update' : 'Create'}</button>
        <button type="button" onClick={() => navigate('/courses')} style={{ marginLeft: 8 }}>Cancel</button>
      </form>
    </div>
  );
};

export default CourseFormPage;