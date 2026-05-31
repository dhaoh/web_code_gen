import { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { fetchCourses, deleteCourse, Course } from '../api';

export default function CourseListPage() {
  const [courses, setCourses] = useState<Course[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const load = () => {
    setLoading(true);
    fetchCourses()
      .then(setCourses)
      .catch(err => setError(err.message))
      .finally(() => setLoading(false));
  };

  useEffect(() => { load(); }, []);

  const handleDelete = async (id: number) => {
    if (!confirm('Are you sure you want to delete this course? Existing enrollments will also be removed.')) return;
    try {
      await deleteCourse(id);
      setCourses(prev => prev.filter(c => c.id !== id));
    } catch (err: any) {
      alert(err.message);
    }
  };

  if (loading) return <p>Loading courses...</p>;
  if (error) return <p style={{ color: 'red' }}>Error: {error}</p>;

  return (
    <div>
      <h2>Courses</h2>
      <button onClick={() => navigate('/courses/new')}>Add Course</button>
      {courses.length === 0 ? (
        <p>No courses yet.</p>
      ) : (
        <table border={1} cellPadding={5} style={{ marginTop: '1rem' }}>
          <thead>
            <tr>
              <th>ID</th>
              <th>Title</th>
              <th>Description</th>
              <th>Capacity</th>
              <th>Enrolled</th>
              <th>Available</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {courses.map(c => (
              <tr key={c.id}>
                <td>{c.id}</td>
                <td>{c.title}</td>
                <td>{c.description || '-'}</td>
                <td>{c.capacity}</td>
                <td>{c.enrolled_count}</td>
                <td>{c.capacity - c.enrolled_count}</td>
                <td>
                  <button onClick={() => navigate(`/courses/edit/${c.id}`)}>Edit</button>
                  <button onClick={() => handleDelete(c.id)} style={{ marginLeft: '0.5rem' }}>Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}