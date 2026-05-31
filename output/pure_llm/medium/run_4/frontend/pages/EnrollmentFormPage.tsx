import React, { useEffect, useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { EnrollmentCreate, createEnrollment, getUsers, getCourses, User, Course } from "../api";

const EnrollmentForm: React.FC = () => {
  const navigate = useNavigate();
  const [error, setError] = useState("");
  const [students, setStudents] = useState<User[]>([]);
  const [courses, setCourses] = useState<Course[]>([]);
  const [form, setForm] = useState<EnrollmentCreate>({ student_id: 0, course_id: 0 });

  useEffect(() => {
    getUsers().then((users) => setStudents(users.filter((u) => u.role === "student"))).catch(() => {});
    getCourses().then(setCourses).catch(() => {});
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setForm({ ...form, [e.target.name]: Number(e.target.value) });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!form.student_id || !form.course_id) {
      alert("Select both student and course");
      return;
    }
    createEnrollment(form)
      .then(() => navigate("/enrollments"))
      .catch((err) => setError(err.message));
  };

  return (
    <div>
      <h2>Create Enrollment</h2>
      {error && <p style={{ color: "red" }}>{error}</p>}
      <form onSubmit={handleSubmit}>
        <div>
          <label>Student:</label>
          <select name="student_id" value={form.student_id} onChange={handleChange} required>
            <option value={0}>-- Select --</option>
            {students.map((s) => (
              <option key={s.id} value={s.id}>{s.full_name}</option>
            ))}
          </select>
        </div>
        <div>
          <label>Course:</label>
          <select name="course_id" value={form.course_id} onChange={handleChange} required>
            <option value={0}>-- Select --</option>
            {courses.map((c) => (
              <option key={c.id} value={c.id}>{c.title} ({c.credits} cr)</option>
            ))}
          </select>
        </div>
        <button type="submit">Enroll</button>
        <Link to="/enrollments">Cancel</Link>
      </form>
    </div>
  );
};

export default EnrollmentForm;