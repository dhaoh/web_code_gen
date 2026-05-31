import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { createCourse, updateCourse, fetchCourse, Course } from '../api';

export default function CourseFormPage() {
  const { id } = useParams();
  const isEdit = !!id;
  const navigate = useNavigate();
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [capacity, setCapacity] = useState<number>(1);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (isEdit) {
      fetchCourse(Number(id))
        .then(c => {
          setTitle(c.title);
          setDescription(c.description || '');
          setCapacity(c.capacity);
        })
        .catch(err => setError(err.message));
    }
  }, [id]);

  const validate = (): boolean => {
    if (!title.trim()) {
      setError('Title is required');
      return false;
    }
    if (capacity < 1) {
      setError('Capacity must be at least 1');
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
      const data = { title, description: description || undefined, capacity };
      if (isEdit) {
        await updateCourse(Number(id), data);
      } else {
        await createCourse(data);
      }
      navigate('/courses');
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>{isEdit ? 'Edit Course' : 'Add Course'}</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <form onSubmit={handleSubmit}>
        <div>
          <label>Title: </label>
          <input value={title} onChange={e => setTitle(e.target.value)} required />
        </div>
        <div style={{ marginTop: '0.5rem' }}>
          <label>Description: </label>
          <textarea value={description} onChange={e => setDescription(e.target.value)} />
        </div>
        <div style={{ marginTop: '0.5rem' }}>
          <label>Capacity: </label>
          <input type="number" min="1" value={capacity} onChange={e => setCapacity(Number(e.target.value))} required />
        </div>
        <div style={{ marginTop: '1rem' }}>
          <button type="submit" disabled={loading}>
            {loading ? 'Saving...' : 'Save'}
          </button>
          <button type="button" onClick={() => navigate('/courses')} style={{ marginLeft: '0.5rem' }}>
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
}