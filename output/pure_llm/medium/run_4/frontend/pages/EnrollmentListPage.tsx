import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Enrollment, getEnrollments, deleteEnrollment } from "../api";

const EnrollmentList: React.FC = () => {
  const [enrollments, setEnrollments] = useState<Enrollment[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    getEnrollments()
      .then(setEnrollments)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  const handleDelete = (id: number) => {
    if (window.confirm("Delete this enrollment?")) {
      deleteEnrollment(id)
        .then(() => setEnrollments(enrollments.filter((e) => e.id !== id)))
        .catch((err) => alert(err.message));
    }
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div>
      <h2>Enrollments</h2>
      <Link to="/enrollments/new">Create New Enrollment</Link>
      {enrollments.length === 0 ? (
        <p>No enrollments found.</p>
      ) : (
        <table border={1}>
          <thead>
            <tr>
              <th>ID</th>
              <th>Student ID</th>
              <th>Course ID</th>
              <th>Enrolled At</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {enrollments.map((e) => (
              <tr key={e.id}>
                <td>{e.id}</td>
                <td>{e.student_id}</td>
                <td>{e.course_id}</td>
                <td>{new Date(e.enrolled_at).toLocaleString()}</td>
                <td>
                  <button onClick={() => handleDelete(e.id)}>Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default EnrollmentList;