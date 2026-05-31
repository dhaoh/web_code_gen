import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Course, getCourses, deleteCourse } from "../api";

const CourseList: React.FC = () => {
  const [courses, setCourses] = useState<Course[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    getCourses()
      .then(setCourses)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  const handleDelete = (id: number) => {
    if (window.confirm("Delete this course?")) {
      deleteCourse(id)
        .then(() => setCourses(courses.filter((c) => c.id !== id)))
        .catch((err) => alert(err.message));
    }
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div>
      <h2>Courses</h2>
      <Link to="/courses/new">Create New Course</Link>
      {courses.length === 0 ? (
        <p>No courses found.</p>
      ) : (
        <table border={1}>
          <thead>
            <tr>
              <th>ID</th>
              <th>Title</th>
              <th>Credits</th>
              <th>Capacity</th>
              <th>Department ID</th>
              <th>Teacher ID</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {courses.map((c) => (
              <tr key={c.id}>
                <td>{c.id}</td>
                <td>{c.title}</td>
                <td>{c.credits}</td>
                <td>{c.capacity}</td>
                <td>{c.department_id}</td>
                <td>{c.teacher_id ?? "None"}</td>
                <td>
                  <Link to={`/courses/${c.id}/edit`}>Edit</Link>{" "}
                  <button onClick={() => handleDelete(c.id)}>Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default CourseList;