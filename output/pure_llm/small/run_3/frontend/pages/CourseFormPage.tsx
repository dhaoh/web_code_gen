import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { CourseCreate, getCourse, createCourse, updateCourse } from '../api';

const CourseFormPage: React.FC = () => {
  const { id } = useParams();
  const isEdit = Boolean(id);
  const navigate = useNavigate();

  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [capacity, setCapacity] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (isEdit) {
      const fetchCourse = async () => {
        try {
          setLoading(true);
          const course = await getCourse(Number(id));
          setTitle(course.title);
          setDescription(course.description || '');
          setCapacity(course.capacity);
        } catch (err: any) {
          setError(err.message);
        } finally {
          setLoading(false);
        }
      };
      fetchCourse();
    }
  }, [id, isEdit]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) {
      alert('Title is required');
      return;
    }
    if (capacity < 1) {
      alert('Capacity must be at least 1');
      return;
    }
    const data: CourseCreate = {
      title: title.trim(),
      description: description.trim() || undefined,
      capacity,
    };
    try {
      setLoading(true);
      if (isEdit) {
        await updateCourse(Number(id), data);
      } else {
        await createCourse(data);
      }
      navigate('/courses');
    } catch (err: any) {
      setError(err.message);
      setLoading(false);
    }
  };

  if (loading && isEdit) return <p>Loading...</p>;
  if (error) return <p style={{ color: 'red' }}>Error: {error}</p>;

  return (
    <div>
      <h2>{isEdit ? 'Edit Course' : 'Add Course'}</h2>
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
        <div style={{ marginTop: 8 }}>
          <label>Description:</label>
          <textarea
            value={description}
            onChange={e => setDescription(e.target.value)}
            rows={3}
          />
        </div>
        <div style={{ marginTop: 8 }}>
          <label>Capacity:</label>
          <input
            type="number"
            value={capacity}
            onChange={e => setCapacity(Number(e.target.value))}
            min={1}
            required
          />
        </div>
        <div style={{ marginTop: 16 }}>
          <button type="submit" disabled={loading}>
            {loading ? 'Saving...' : 'Save'}
          </button>
          <button type="button" onClick={() => navigate('/courses')} style={{ marginLeft: 8 }}>
            Cancel
          </button>
        </div>
        {error && <p style={{ color: 'red' }}>{error}</p>}
      </form>
    </div>
  );
};

export default CourseFormPage;