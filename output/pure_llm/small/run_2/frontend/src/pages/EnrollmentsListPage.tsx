import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { enrollmentApi, Enrollment } from '../api';

const EnrollmentsListPage: React.FC = () => {
  const [enrollments, setEnrollments] = useState<Enrollment[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadEnrollments();
  }, []);

  const loadEnrollments = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await enrollmentApi.getAll();
      setEnrollments(data);
    } catch (err: any) {
      setError(err.message || 'Failed to load enrollments');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (!window.confirm('Are you sure you want to delete this enrollment?')) {
      return;
    }
    try {
      await enrollmentApi.delete(id);
      setEnrollments(enrollments.filter(e => e.id !== id));
    } catch (err: any) {
      alert(err.message || 'Failed to delete enrollment');
    }
  };

  if (loading) {
    return <div style={styles.loading}>Loading enrollments...</div>;
  }

  if (error) {
    return (
      <div style={styles.error}>
        <p>Error: {error}</p>
        <button onClick={loadEnrollments} style={styles.retryButton}>Retry</button>
      </div>
    );
  }

  return (
    <div>
      <div style={styles.header}>
        <h2>Enrollments</h2>
        <Link to="/enrollments/new" style={styles.addButton}>New Enrollment</Link>
      </div>
      
      {enrollments.length === 0 ? (
        <div style={styles.empty}>
          <p>No enrollments found.</p>
          <p>Click "New Enrollment" to enroll a student in a course.</p>
        </div>
      ) : (
        <table style={styles.table}>
          <thead>
            <tr>
              <th style={styles.th}>ID</th>
              <th style={styles.th}>Student</th>
              <th style={styles.th}>Course</th>
              <th style={styles.th}>Enrolled At</th>
              <th style={styles.th}>Actions</th>
            </tr>
          </thead>
          <tbody>
            {enrollments.map(enrollment => (
              <tr key={enrollment.id}>
                <td style={styles.td}>{enrollment.id}</td>
                <td style={styles.td}>{enrollment.student?.name || 'N/A'}</td>
                <td style={styles.td}>{enrollment.course?.title || 'N/A'}</td>
                <td style={styles.td}>
                  {new Date(enrollment.enrolled_at).toLocaleString()}
                </td>
                <td style={styles.td}>
                  <button
                    onClick={() => handleDelete(enrollment.id)}
                    style={styles.deleteButton}
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

const styles: { [key: string]: React.CSSProperties } = {
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '20px',
  },
  loading: {
    textAlign: 'center',
    padding: '40px',
    fontSize: '18px',
    color: '#666',
  },
  error: {
    textAlign: 'center',
    padding: '40px',
    color: '#dc3545',
  },
  retryButton: {
    padding: '8px 16px',
    backgroundColor: '#007bff',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
  },
  empty: {
    textAlign: 'center',
    padding: '40px',
    color: '#666',
  },
  addButton: {
    padding: '10px 20px',
    backgroundColor: '#28a745',
    color: 'white',
    textDecoration: 'none',
    borderRadius: '4px',
    fontWeight: 'bold',
  },
  table: {
    width: '100%',
    borderCollapse: 'collapse',
  },
  th: {
    backgroundColor: '#f8f9fa',
    padding: '12px',
    textAlign: 'left',
    borderBottom: '2px solid #dee2e6',
    fontWeight: 'bold',
  },
  td: {
    padding: '12px',
    borderBottom: '1px solid #dee2e6',
  },
  deleteButton: {
    padding: '6px 12px',
    backgroundColor: '#dc3545',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
  },
};

export default EnrollmentsListPage;