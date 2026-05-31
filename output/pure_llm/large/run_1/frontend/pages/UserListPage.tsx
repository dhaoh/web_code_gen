import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api";

export default function UserListPage() {
  const [users, setUsers] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const fetchUsers = async () => {
    try {
      const data = await api.getUsers();
      setUsers(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchUsers(); }, []);

  const handleDelete = async (id: number) => {
    if (!window.confirm("Delete?")) return;
    try {
      await api.deleteUser(id);
      setUsers(users.filter(u => u.id !== id));
    } catch (err: any) {
      alert(err.message);
    }
  };

  if (loading) return <p>Loading...</p>;
  if (error) return <p style={{color:"red"}}>{error}</p>;

  return (
    <div>
      <h2>Users</h2>
      <Link to="/users/new">Create New</Link>
      {users.length === 0 ? <p>No users found.</p> : (
        <table border={1} cellPadding={5}>
          <thead>
            <tr>
              <th>ID</th><th>Username</th><th>Role</th><th>Full Name</th><th>Email</th><th>Major</th><th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {users.map((u: any) => (
              <tr key={u.id}>
                <td>{u.id}</td><td>{u.username}</td><td>{u.role}</td><td>{u.full_name}</td><td>{u.email}</td><td>{u.major_id}</td>
                <td>
                  <Link to={`/users/${u.id}/edit`}>Edit</Link> |{" "}
                  <button onClick={() => handleDelete(u.id)}>Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}