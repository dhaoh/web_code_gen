import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { fetchEnrollments, deleteEnrollment, Enrollment } from '../api';

const EnrollmentListPage: React.FC = () => {
  const [enrollments, setEnrollments] = useState<Enrollment[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const load = async () => {
    try {
      setLoading(true);
      setError('');
      const data = await fetchEnrollments();
      setEnrollments(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  const handleDelete = async (id: number) => {
    if (!window.confirm('Drop enrollment?')) return;
    try {
      await deleteEnrollment(id);
      setEnrollments(prev => prev.filter(e => e.id !== id));
    } catch (err: any) {
      alert(err.message);
    }
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div style={{ color: 'red' }}>Error: {error}</div>;

  return (
    <div>
      <h2>Enrollments</h2>
      <button onClick={() => navigate('/enrollments/new')}>New Enrollment</button>
      {enrollments.length === 0 ? (
        <p>No enrollments yet.</p>
      ) : (
        <table border={1} cellPadding={8} style={{ marginTop: '1rem' }}>
          <thead>
            <tr>
              <th>ID</th>
              <th>Student</th>
              <th>Course</th>
              <th>Enrolled At</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {enrollments.map(e => (
              <tr key={e.id}>
                <td>{e.id}</td>
                <td>{e.student_name}</td>
                <td>{e.course_title}</td>
                <td>{new Date(e.enrolled_at).toLocaleString()}</td>
                <td>
                  <button onClick={() => handleDelete(e.id)}>Drop</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default EnrollmentListPage;