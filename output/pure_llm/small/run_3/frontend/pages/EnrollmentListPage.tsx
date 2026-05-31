import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Enrollment, getEnrollments, deleteEnrollment } from '../api';

const EnrollmentListPage: React.FC = () => {
  const [enrollments, setEnrollments] = useState<Enrollment[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchEnrollments = async () => {
    try {
      setLoading(true);
      const data = await getEnrollments();
      setEnrollments(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchEnrollments();
  }, []);

  const handleDelete = async (id: number) => {
    if (!window.confirm('Are you sure you want to remove this enrollment?')) return;
    try {
      await deleteEnrollment(id);
      setEnrollments(enrollments.filter(e => e.id !== id));
    } catch (err: any) {
      alert(err.message);
    }
  };

  if (loading) return <p>Loading...</p>;
  if (error) return <p style={{ color: 'red' }}>Error: {error}</p>;

  return (
    <div>
      <h2>Enrollments</h2>
      <Link to="/enrollments/new">Add Enrollment</Link>
      {enrollments.length === 0 ? (
        <p>No enrollments found.</p>
      ) : (
        <table border={1} cellPadding={8} style={{ marginTop: 10, width: '100%' }}>
          <thead>
            <tr>
              <th>ID</th>
              <th>Student</th>
              <th>Course</th>
              <th>Enrolled At</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {enrollments.map(enr => (
              <tr key={enr.id}>
                <td>{enr.id}</td>
                <td>{enr.student_name}</td>
                <td>{enr.course_title}</td>
                <td>{new Date(enr.enrolled_at).toLocaleString()}</td>
                <td>
                  <button onClick={() => handleDelete(enr.id)}>Delete</button>
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