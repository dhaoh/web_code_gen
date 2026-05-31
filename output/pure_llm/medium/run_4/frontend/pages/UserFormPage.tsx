import React, { useEffect, useState } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import { User, UserCreate, getUser, createUser, updateUser } from "../api";

const UserForm: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const isEdit = !!id;
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [form, setForm] = useState<UserCreate & { id?: number }>({
    username: "",
    password: "",
    role: "student",
    full_name: "",
    email: "",
  });

  useEffect(() => {
    if (isEdit) {
      setLoading(true);
      getUser(Number(id))
        .then((user) =>
          setForm({
            id: user.id,
            username: user.username,
            password: "",
            role: user.role,
            full_name: user.full_name,
            email: user.email,
          })
        )
        .catch((err) => setError(err.message))
        .finally(() => setLoading(false));
    }
  }, [id, isEdit]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!form.username || !form.email || !form.full_name) {
      alert("Please fill all required fields");
      return;
    }
    if (!isEdit && !form.password) {
      alert("Password required");
      return;
    }
    const data: any = { ...form };
    if (isEdit) {
      delete data.id;
      delete data.username;
      updateUser(Number(id), {
        full_name: form.full_name,
        email: form.email,
        role: form.role,
      })
        .then(() => navigate("/users"))
        .catch((err) => setError(err.message));
    } else {
      createUser(data as UserCreate)
        .then(() => navigate("/users"))
        .catch((err) => setError(err.message));
    }
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div>
      <h2>{isEdit ? "Edit User" : "Create User"}</h2>
      <form onSubmit={handleSubmit}>
        {!isEdit && (
          <div>
            <label>Username:</label>
            <input name="username" value={form.username} onChange={handleChange} required />
          </div>
        )}
        {!isEdit && (
          <div>
            <label>Password:</label>
            <input type="password" name="password" value={form.password} onChange={handleChange} required />
          </div>
        )}
        <div>
          <label>Full Name:</label>
          <input name="full_name" value={form.full_name} onChange={handleChange} required />
        </div>
        <div>
          <label>Email:</label>
          <input type="email" name="email" value={form.email} onChange={handleChange} required />
        </div>
        <div>
          <label>Role:</label>
          <select name="role" value={form.role} onChange={handleChange}>
            <option value="student">Student</option>
            <option value="teacher">Teacher</option>
          </select>
        </div>
        <button type="submit">{isEdit ? "Update" : "Create"}</button>
        <Link to="/users">Cancel</Link>
      </form>
    </div>
  );
};

export default UserForm;