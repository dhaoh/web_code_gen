import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import * as api from "../api";

interface Enrollment {
  id: number;
  student_id: number;
  course_id: number;
  enrolled_at: string;
}

export default function EnrollmentListPage() {
  const [enrollments, setEnrollments] = useState<Enrollment[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  const fetchEnrollments = async () => {
    try {
      setLoading(true);
      const data = await api.getEnrollments();
      setEnrollments(data);
      setError(null);
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
    if (!window.confirm("Are you sure you want to delete this enrollment?")) return;
    try {
      await api.deleteEnrollment(id);
      setEnrollments(enrollments.filter(e => e.id !== id));
    } catch (err: any) {
      alert("Failed to delete enrollment: " + err.message);
    }
  };

  if (loading) return <div className="text-center py-10">Loading enrollments...</div>;
  if (error) return <div className="text-red-600">Error: {error}</div>;

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Enrollments</h1>
      <button
        onClick={() => navigate("/enrollments/new")}
        className="bg-blue-500 text-white px-4 py-2 rounded mb-4"
      >
        New Enrollment
      </button>
      {enrollments.length === 0 ? (
        <p className="text-gray-500">No enrollments found.</p>
      ) : (
        <table className="w-full border">
          <thead className="bg-gray-200">
            <tr>
              <th className="p-2 text-left">ID</th>
              <th className="p-2 text-left">Student ID</th>
              <th className="p-2 text-left">Course ID</th>
              <th className="p-2 text-left">Enrolled At</th>
              <th className="p-2">Actions</th>
            </tr>
          </thead>
          <tbody>
            {enrollments.map(e => (
              <tr key={e.id} className="border-t">
                <td className="p-2">{e.id}</td>
                <td className="p-2">{e.student_id}</td>
                <td className="p-2">{e.course_id}</td>
                <td className="p-2">{new Date(e.enrolled_at).toLocaleString()}</td>
                <td className="p-2 text-center">
                  <button
                    onClick={() => handleDelete(e.id)}
                    className="bg-red-500 text-white px-3 py-1 rounded"
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
}