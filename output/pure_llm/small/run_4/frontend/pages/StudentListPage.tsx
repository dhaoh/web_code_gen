import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { fetchStudents, deleteStudent } from '../api';

interface Student {
  id: number;
  name: string;
  email: string;
}

const StudentListPage: React.FC = () => {
  const [students, setStudents] = useState<Student[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadStudents = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await fetchStudents();
      setStudents(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadStudents();
  }, []);

  const handleDelete = async (id: number) => {
    if (!window.confirm('Are you sure?')) return;
    try {
      await deleteStudent(id);
      setStudents(students.filter(s => s.id !== id));
    } catch (err: any) {
      alert(err.message);
    }
  };

  if (loading) return <div>Loading students...</div>;
  if (error) return <div style={{ color: 'red' }}>Error: {error} <button onClick={loadStudents}>Retry</button></div>;
  if (students.length === 0) return <div>No students found. <Link to="/students/new">Add a student</Link></div>;

  return (
    <div>
      <h2>Students</h2>
      <Link to="/students/new">Add New Student</Link>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Email</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {students.map(student => (
            <tr key={student.id}>
              <td>{student.id}</td>
              <td>{student.name}</td>
              <td>{student.email}</td>
              <td>
                <Link to={`/students/${student.id}/edit`}>Edit</Link>
                <button onClick={() => handleDelete(student.id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default StudentListPage;