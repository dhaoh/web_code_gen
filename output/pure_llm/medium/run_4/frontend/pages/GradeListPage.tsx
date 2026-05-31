import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Grade, getGrades, deleteGrade } from "../api";

const GradeList: React.FC = () => {
  const [grades, setGrades] = useState<Grade[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    getGrades()
      .then(setGrades)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  const handleDelete = (id: number) => {
    if (window.confirm("Delete this grade?")) {
      deleteGrade(id)
        .then(() => setGrades(grades.filter((g) => g.id !== id)))
        .catch((err) => alert(err.message));
    }
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div>
      <h2>Grades</h2>
      <Link to="/grades/new">Assign New Grade</Link>
      {grades.length === 0 ? (
        <p>No grades found.</p>
      ) : (
        <table border={1}>
          <thead>
            <tr>
              <th>ID</th>
              <th>Enrollment ID</th>
              <th>Score</th>
              <th>Letter</th>
              <th>Graded At</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {grades.map((g) => (
              <tr key={g.id}>
                <td>{g.id}</td>
                <td>{g.enrollment_id}</td>
                <td>{g.score}</td>
                <td>{g.letter_grade || "-"}</td>
                <td>{g.graded_at ? new Date(g.graded_at).toLocaleString() : "-"}</td>
                <td>
                  <Link to={`/grades/${g.id}/edit`}>Edit</Link>{" "}
                  <button onClick={() => handleDelete(g.id)}>Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default GradeList;