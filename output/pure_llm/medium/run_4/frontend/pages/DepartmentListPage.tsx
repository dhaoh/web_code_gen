import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Department, getDepartments, deleteDepartment } from "../api";

const DepartmentList: React.FC = () => {
  const [departments, setDepartments] = useState<Department[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    getDepartments()
      .then(setDepartments)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  const handleDelete = (id: number) => {
    if (window.confirm("Delete this department?")) {
      deleteDepartment(id)
        .then(() => setDepartments(departments.filter((d) => d.id !== id)))
        .catch((err) => alert(err.message));
    }
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div>
      <h2>Departments</h2>
      <Link to="/departments/new">Create New Department</Link>
      {departments.length === 0 ? (
        <p>No departments found.</p>
      ) : (
        <table border={1}>
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Code</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {departments.map((d) => (
              <tr key={d.id}>
                <td>{d.id}</td>
                <td>{d.name}</td>
                <td>{d.code}</td>
                <td>
                  <Link to={`/departments/${d.id}/edit`}>Edit</Link>{" "}
                  <button onClick={() => handleDelete(d.id)}>Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default DepartmentList;