import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { fetchStudents, fetchCourses, createEnrollment, Student, Course } from '../api';

export default function EnrollmentFormPage() {
  const navigate = useNavigate();
  const [students, setStudents] = useState<Student[]>([]);
  const [courses, setCourses] = useState<Course[]>([]);
  const [studentId, setStudentId] = useState<number | ''>('');
  const [courseId, setCourseId] = useState<number | ''>('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    const loadData = async () => {
      try {
        const [s, c] = await Promise.all([fetchStudents(), fetchCourses()]);
        setStudents(s);
        setCourses(c);
      } catch (err: any) {
        setError(err.message);
      }
    };
    loadData();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (studentId === '' || courseId === '') {
      setError('Please select a student and a course.');
      return;
    }
    setLoading(true);
    setError('');
    try {
      await createEnrollment({ student_id: Number(studentId), course_id: Number(courseId) });
      navigate('/enrollments');
    } catch (err: any) {
      setError(err.message);
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>Add Enrollment</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <form onSubmit={handleSubmit}>
        <div>
          <label>Student:</label>
          <select value={studentId} onChange={e => setStudentId(e.target.value ? Number(e.target.value) : '')} required>
            <option value="">-- Select Student --</option>
            {students.map(s => (
              <option key={s.id} value={s.id}>{s.name} ({s.email})</option>
            ))}
          </select>
        </div>
        <div>
          <label>Course:</label>
          <select value={courseId} onChange={e => setCourseId(e.target.value ? Number(e.target.value) : '')} required>
            <option value="">-- Select Course --</option>
            {courses.map(c => (
              <option key={c.id} value={c.id}>{c.title} (Capacity: {c.capacity})</option>
            ))}
          </select>
        </div>
        <button type="submit" disabled={loading}>Enroll</button>
        <button type="button" onClick={() => navigate('/enrollments')}>Cancel</button>
      </form>
    </div>
  );
}