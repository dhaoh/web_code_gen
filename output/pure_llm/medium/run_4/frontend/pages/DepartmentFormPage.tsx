import React, { useEffect, useState } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import { Department, getDepartment, createDepartment, updateDepartment } from "../api";

const DepartmentForm: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const isEdit = !!id;
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [form, setForm] = useState({ name: "", code: "" });

  useEffect(() => {
    if (isEdit) {
      setLoading(true);
      getDepartment(Number(id))
        .then((dept) => setForm({ name: dept.name, code: dept.code }))
        .catch((err) => setError(err.message))
        .finally(() => setLoading(false));
    }
  }, [id, isEdit]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!form.name || !form.code) {
      alert("All fields required");
      return;
    }
    if (isEdit) {
      updateDepartment(Number(id), form)
        .then(() => navigate("/departments"))
        .catch((err) => setError(err.message));
    } else {
      createDepartment(form)
        .then(() => navigate("/departments"))
        .catch((err) => setError(err.message));
    }
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div>
      <h2>{isEdit ? "Edit Department" : "Create Department"}</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Name:</label>
          <input name="name" value={form.name} onChange={handleChange} required />
        </div>
        <div>
          <label>Code:</label>
          <input name="code" value={form.code} onChange={handleChange} required />
        </div>
        <button type="submit">{isEdit ? "Update" : "Create"}</button>
        <Link to="/departments">Cancel</Link>
      </form>
    </div>
  );
};

export default DepartmentForm;