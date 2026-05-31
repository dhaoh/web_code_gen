import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getStudents, getCourses, createEnrollment, Student, Course, EnrollmentCreate } from '../api';

const EnrollmentFormPage: React.FC = () => {
  const navigate = useNavigate();
  const [students, setStudents] = useState<Student[]>([]);
  const [courses, setCourses] = useState<Course[]>([]);
  const [studentId, setStudentId] = useState<number | ''>('');
  const [courseId, setCourseId] = useState<number | ''>('');
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const [studentsData, coursesData] = await Promise.all([getStudents(), getCourses()]);
        setStudents(studentsData);
        setCourses(coursesData);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (studentId === '' || courseId === '') {
      alert('Please select both student and course');
      return;
    }
    const data: EnrollmentCreate = {
      student_id: Number(studentId),
      course_id: Number(courseId),
    };
    try {
      setSubmitting(true);
      await createEnrollment(data);
      navigate('/enrollments');
    } catch (err: any) {
      setError(err.message);
      setSubmitting(false);
    }
  };

  if (loading) return <p>Loading students and courses...</p>;
  if (error && !submitting) return <p style={{ color: 'red' }}>Error: {error}</p>;

  return (
    <div>
      <h2>New Enrollment</h2>
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
        <div style={{ marginTop: 8 }}>
          <label>Course:</label>
          <select value={courseId} onChange={e => setCourseId(e.target.value ? Number(e.target.value) : '')} required>
            <option value="">-- Select Course --</option>
            {courses.map(c => (
              <option key={c.id} value={c.id}>{c.title} (capacity: {c.capacity})</option>
            ))}
          </select>
        </div>
        <div style={{ marginTop: 16 }}>
          <button type="submit" disabled={submitting}>
            {submitting ? 'Enrolling...' : 'Enroll'}
          </button>
          <button type="button" onClick={() => navigate('/enrollments')} style={{ marginLeft: 8 }}>
            Cancel
          </button>
        </div>
        {error && submitting && <p style={{ color: 'red' }}>{error}</p>}
      </form>
    </div>
  );
};

export default EnrollmentFormPage;