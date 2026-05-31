import React, { useEffect, useState } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import { Course, CourseCreate, getCourse, createCourse, updateCourse, getDepartments, getUsers, Department, User } from "../api";

const CourseForm: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const isEdit = !!id;
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [departments, setDepartments] = useState<Department[]>([]);
  const [teachers, setTeachers] = useState<User[]>([]);
  const [form, setForm] = useState<CourseCreate>({
    title: "",
    description: "",
    capacity: 0,
    credits: 0,
    department_id: 0,
    teacher_id: undefined,
  });

  useEffect(() => {
    getDepartments().then(setDepartments).catch(() => {});
    getUsers().then((users) => setTeachers(users.filter((u) => u.role === "teacher"))).catch(() => {});
  }, []);

  useEffect(() => {
    if (isEdit) {
      setLoading(true);
      getCourse(Number(id))
        .then((course) =>
          setForm({
            title: course.title,
            description: course.description || "",
            capacity: course.capacity,
            credits: course.credits,
            department_id: course.department_id,
            teacher_id: course.teacher_id,
          })
        )
        .catch((err) => setError(err.message))
        .finally(() => setLoading(false));
    }
  }, [id, isEdit]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setForm({ ...form, [name]: name === "teacher_id" ? (value ? Number(value) : undefined) : value });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!form.title || !form.credits || !form.capacity || !form.department_id) {
      alert("Required fields missing");
      return;
    }
    if (isEdit) {
      updateCourse(Number(id), form)
        .then(() => navigate("/courses"))
        .catch((err) => setError(err.message));
    } else {
      createCourse(form as CourseCreate)
        .then(() => navigate("/courses"))
        .catch((err) => setError(err.message));
    }
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div>
      <h2>{isEdit ? "Edit Course" : "Create Course"}</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Title:</label>
          <input name="title" value={form.title} onChange={handleChange} required />
        </div>
        <div>
          <label>Description:</label>
          <textarea name="description" value={form.description} onChange={handleChange} />
        </div>
        <div>
          <label>Capacity:</label>
          <input type="number" name="capacity" value={form.capacity} onChange={handleChange} required />
        </div>
        <div>
          <label>Credits:</label>
          <input type="number" name="credits" value={form.credits} onChange={handleChange} required />
        </div>
        <div>
          <label>Department:</label>
          <select name="department_id" value={form.department_id} onChange={handleChange} required>
            <option value={0}>-- Select --</option>
            {departments.map((d) => (
              <option key={d.id} value={d.id}>{d.name}</option>
            ))}
          </select>
        </div>
        <div>
          <label>Teacher:</label>
          <select name="teacher_id" value={form.teacher_id || ""} onChange={handleChange}>
            <option value="">-- None --</option>
            {teachers.map((t) => (
              <option key={t.id} value={t.id}>{t.full_name}</option>
            ))}
          </select>
        </div>
        <button type="submit">{isEdit ? "Update" : "Create"}</button>
        <Link to="/courses">Cancel</Link>
      </form>
    </div>
  );
};

export default CourseForm;