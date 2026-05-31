import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import * as api from "../api";

export default function CourseFormPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const isEdit = Boolean(id);

  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [capacity, setCapacity] = useState<number>(10);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [fetching, setFetching] = useState(isEdit);

  useEffect(() => {
    if (!isEdit) return;
    const fetchCourse = async () => {
      try {
        const course = await api.getCourse(Number(id));
        setTitle(course.title);
        setDescription(course.description || "");
        setCapacity(course.capacity);
      } catch (err: any) {
        setError("Failed to load course data");
      } finally {
        setFetching(false);
      }
    };
    fetchCourse();
  }, [id, isEdit]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    if (!title.trim()) {
      setError("Title is required");
      return;
    }
    if (capacity < 1) {
      setError("Capacity must be at least 1");
      return;
    }

    setLoading(true);
    try {
      const data = {
        title: title.trim(),
        description: description.trim() || null,
        capacity: capacity,
      };
      if (isEdit) {
        await api.updateCourse(Number(id), data);
      } else {
        await api.createCourse(data);
      }
      navigate("/courses");
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  if (fetching) return <div>Loading course...</div>;

  return (
    <div className="max-w-md mx-auto">
      <h1 className="text-2xl font-bold mb-4">{isEdit ? "Edit Course" : "Add Course"}</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block font-medium mb-1">Title *</label>
          <input
            type="text"
            value={title}
            onChange={e => setTitle(e.target.value)}
            className="w-full border p-2 rounded"
            required
          />
        </div>
        <div>
          <label className="block font-medium mb-1">Description</label>
          <textarea
            value={description}
            onChange={e => setDescription(e.target.value)}
            className="w-full border p-2 rounded"
          />
        </div>
        <div>
          <label className="block font-medium mb-1">Capacity *</label>
          <input
            type="number"
            min="1"
            value={capacity}
            onChange={e => setCapacity(parseInt(e.target.value) || 0)}
            className="w-full border p-2 rounded"
            required
          />
        </div>
        {error && <p className="text-red-600">{error}</p>}
        <div className="flex gap-4">
          <button
            type="submit"
            disabled={loading}
            className="bg-blue-500 text-white px-4 py-2 rounded disabled:opacity-50"
          >
            {loading ? "Saving..." : "Save"}
          </button>
          <button
            type="button"
            onClick={() => navigate("/courses")}
            className="bg-gray-300 px-4 py-2 rounded"
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
}