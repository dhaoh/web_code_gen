import React, { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import * as api from "../api";

interface Course {
  id: number;
  title: string;
  description: string | null;
  capacity: number;
}

export default function CourseListPage() {
  const [courses, setCourses] = useState<Course[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  const fetchCourses = async () => {
    try {
      setLoading(true);
      const data = await api.getCourses();
      setCourses(data);
      setError(null);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCourses();
  }, []);

  const handleDelete = async (id: number) => {
    if (!window.confirm("Are you sure you want to delete this course?")) return;
    try {
      await api.deleteCourse(id);
      setCourses(courses.filter(c => c.id !== id));
    } catch (err: any) {
      alert("Failed to delete course: " + err.message);
    }
  };

  if (loading) return <div className="text-center py-10">Loading courses...</div>;
  if (error) return <div className="text-red-600">Error: {error}</div>;

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Courses</h1>
      <button
        onClick={() => navigate("/courses/new")}
        className="bg-blue-500 text-white px-4 py-2 rounded mb-4"
      >
        Add Course
      </button>
      {courses.length === 0 ? (
        <p className="text-gray-500">No courses found.</p>
      ) : (
        <table className="w-full border">
          <thead className="bg-gray-200">
            <tr>
              <th className="p-2 text-left">ID</th>
              <th className="p-2 text-left">Title</th>
              <th className="p-2 text-left">Description</th>
              <th className="p-2 text-left">Capacity</th>
              <th className="p-2">Actions</th>
            </tr>
          </thead>
          <tbody>
            {courses.map(c => (
              <tr key={c.id} className="border-t">
                <td className="p-2">{c.id}</td>
                <td className="p-2">{c.title}</td>
                <td className="p-2">{c.description || "-"}</td>
                <td className="p-2">{c.capacity}</td>
                <td className="p-2 flex gap-2 justify-center">
                  <button
                    onClick={() => navigate(`/courses/${c.id}/edit`)}
                    className="bg-yellow-500 text-white px-3 py-1 rounded"
                  >
                    Edit
                  </button>
                  <button
                    onClick={() => handleDelete(c.id)}
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