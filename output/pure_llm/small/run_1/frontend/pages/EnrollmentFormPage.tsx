import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import * as api from "../api";

interface Student {
  id: number;
  name: string;
  email: string;
}

interface Course {
  id: number;
  title: string;
  capacity: number;
}

export default function EnrollmentFormPage() {
  const navigate = useNavigate();

  const [students, setStudents] = useState<Student[]>([]);
  const [courses, setCourses] = useState<Course[]>([]);
  const [loadingOptions, setLoadingOptions] = useState(true);
  const [errorOptions, setErrorOptions] = useState<string | null>(null);

  const [studentId, setStudentId] = useState<number | "">("");
  const [courseId, setCourseId] = useState<number | "">("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchOptions = async () => {
      try {
        const [studentsRes, coursesRes] = await Promise.all([
          api.getStudents(),
          api.getCourses(),
        ]);
        setStudents(studentsRes);
        setCourses(coursesRes);
      } catch (err: any) {
        setErrorOptions("Failed to load students or courses");
      } finally {
        setLoadingOptions(false);
      }
    };
    fetchOptions();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    if (!studentId || !courseId) {
      setError("Please select both student and course");
      return;
    }

    setSubmitting(true);
    try {
      await api.createEnrollment({ student_id: Number(studentId), course_id: Number(courseId) });
      navigate("/enrollments");
    } catch (err: any) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  if (loadingOptions) return <div className="text-center py-10">Loading students and courses...</div>;
  if (errorOptions) return <div className="text-red-600">{errorOptions}</div>;

  return (
    <div className="max-w-md mx-auto">
      <h1 className="text-2xl font-bold mb-4">New Enrollment</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block font-medium mb-1">Student *</label>
          <select
            value={studentId}
            onChange={e => setStudentId(e.target.value ? Number(e.target.value) : "")}
            className="w-full border p-2 rounded"
            required
          >
            <option value="">-- Select Student --</option>
            {students.map(s => (
              <option key={s.id} value={s.id}>
                {s.name} ({s.email})
              </option>
            ))}
          </select>
        </div>
        <div>
          <label className="block font-medium mb-1">Course *</label>
          <select
            value={courseId}
            onChange={e => setCourseId(e.target.value ? Number(e.target.value) : "")}
            className="w-full border p-2 rounded"
            required
          >
            <option value="">-- Select Course --</option>
            {courses.map(c => (
              <option key={c.id} value={c.id}>
                {c.title} (capacity: {c.capacity})
              </option>
            ))}
          </select>
        </div>
        {error && <p className="text-red-600">{error}</p>}
        <div className="flex gap-4">
          <button
            type="submit"
            disabled={submitting}
            className="bg-blue-500 text-white px-4 py-2 rounded disabled:opacity-50"
          >
            {submitting ? "Enrolling..." : "Enroll"}
          </button>
          <button
            type="button"
            onClick={() => navigate("/enrollments")}
            className="bg-gray-300 px-4 py-2 rounded"
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
}