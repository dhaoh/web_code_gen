import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { fetchStudents, fetchCourses, createEnrollment, Student, Course } from '../api';

const EnrollmentFormPage: React.FC = () => {
  const navigate = useNavigate();
  const [students, setStudents] = useState<Student[]>([]);
  const [courses, setCourses] = useState<Course[]>([]);
  const [studentId, setStudentId] = useState<number | ''>('');
  const [courseId, setCourseId] = useState<number | ''>('');
  const [loadingData, setLoadingData] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const loadData = async () => {
      try {
        const [studentList, courseList] = await Promise.all([fetchStudents(), fetchCourses()]);
        setStudents(studentList);
        setCourses(courseList);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoadingData(false);
      }
    };
    loadData();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (studentId === '' || courseId === '') {
      setError('Please select both student and course');
      return;
    }
    setError('');
    try {
      await createEnrollment({ student_id: Number(studentId), course_id: Number(courseId) });
      navigate('/enrollments');
    } catch (err: any) {
      setError(err.message);
    }
  };

  if (loadingData) return <div>Loading data...</div>;
  if (error && students.length === 0) return <div style={{ color: 'red' }}>{error}</div>;

  return (
    <div>
      <h2>New Enrollment</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <form onSubmit={handleSubmit}>
        <div>
          <label>Student: </label>
          <select value={studentId} onChange={e => setStudentId(e.target.value ? Number(e.target.value) : '')} required>
            <option value="">-- Select Student --</option>
            {students.map(s => (
              <option key={s.id} value={s.id}>{s.name} ({s.email})</option>
            ))}
          </select>
        </div>
        <div>
          <label>Course: </label>
          <select value={courseId} onChange={e => setCourseId(e.target.value ? Number(e.target.value) : '')} required>
            <option value="">-- Select Course --</option>
            {courses.map(c => (
              <option key={c.id} value={c.id}>{c.title} ({c.enrolled_count}/{c.capacity})</option>
            ))}
          </select>
        </div>
        <button type="submit">Enroll</button>
        <button type="button" onClick={() => navigate('/enrollments')} style={{ marginLeft: 8 }}>Cancel</button>
      </form>
    </div>
  );
};

export default EnrollmentFormPage;