import { useEffect, useState } from 'react';
import { fetchStudents, Student, fetchCourses, Course, fetchEnrollments, Enrollment, createEnrollment, deleteEnrollment } from '../api';

export default function EnrollmentPage() {
  const [students, setStudents] = useState<Student[]>([]);
  const [courses, setCourses] = useState<Course[]>([]);
  const [enrollments, setEnrollments] = useState<Enrollment[]>([]);
  const [selectedStudentId, setSelectedStudentId] = useState<number | null>(null);
  const [loadingStudents, setLoadingStudents] = useState(true);
  const [loadingCourses, setLoadingCourses] = useState(true);
  const [loadingEnrollments, setLoadingEnrollments] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchStudents()
      .then(data => { setStudents(data); if (data.length > 0) setSelectedStudentId(data[0].id); })
      .catch(err => setError(err.message))
      .finally(() => setLoadingStudents(false));

    fetchCourses()
      .then(setCourses)
      .catch(err => setError(err.message))
      .finally(() => setLoadingCourses(false));
  }, []);

  useEffect(() => {
    if (selectedStudentId === null) return;
    setLoadingEnrollments(true);
    fetchEnrollments(selectedStudentId)
      .then(setEnrollments)
      .catch(err => setError(err.message))
      .finally(() => setLoadingEnrollments(false));
  }, [selectedStudentId]);

  const handleEnroll = async (courseId: number) => {
    if (selectedStudentId === null) return;
    setError('');
    try {
      const enrollment = await createEnrollment({ student_id: selectedStudentId, course_id: courseId });
      // update course enrolled_count locally
      setCourses(prev => prev.map(c => c.id === courseId ? { ...c, enrolled_count: c.enrolled_count + 1 } : c));
      // add to enrollments
      setEnrollments(prev => [...prev, enrollment]);
    } catch (err: any) {
      setError(err.message);
    }
  };

  const handleUnenroll = async (enrollmentId: number, courseId: number) => {
    try {
      await deleteEnrollment(enrollmentId);
      setEnrollments(prev => prev.filter(e => e.id !== enrollmentId));
      setCourses(prev => prev.map(c => c.id === courseId ? { ...c, enrolled_count: c.enrolled_count - 1 } : c));
    } catch (err: any) {
      setError(err.message);
    }
  };

  if (loadingStudents || loadingCourses) return <p>Loading...</p>;

  return (
    <div>
      <h2>Enrollment Management</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}

      <div style={{ marginBottom: '1rem' }}>
        <label>Select Student: </label>
        <select value={selectedStudentId ?? ''} onChange={e => setSelectedStudentId(Number(e.target.value))}>
          {students.map(s => (
            <option key={s.id} value={s.id}>{s.name} ({s.email})</option>
          ))}
        </select>
      </div>

      {selectedStudentId && (
        <>
          <h3>Available Courses</h3>
          {courses.length === 0 ? (
            <p>No courses available.</p>
          ) : (
            <table border={1} cellPadding={5} style={{ marginBottom: '2rem' }}>
              <thead>
                <tr>
                  <th>Course</th>
                  <th>Capacity</th>
                  <th>Enrolled</th>
                  <th>Status</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                {courses.map(course => {
                  const enrollment = enrollments.find(e => e.course_id === course.id);
                  const full = course.enrolled_count >= course.capacity;
                  const alreadyEnrolled = !!enrollment;
                  return (
                    <tr key={course.id}>
                      <td>{course.title} {course.description && <small>({course.description})</small>}</td>
                      <td>{course.capacity}</td>
                      <td>{course.enrolled_count}</td>
                      <td>
                        {alreadyEnrolled ? 'Enrolled' : full ? 'Full' : 'Open'}
                      </td>
                      <td>
                        {alreadyEnrolled ? (
                          <button onClick={() => handleUnenroll(enrollment.id, course.id)} style={{ color: 'red' }}>
                            Unenroll
                          </button>
                        ) : (
                          <button onClick={() => handleEnroll(course.id)} disabled={full}>
                            Enroll
                          </button>
                        )}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          )}

          <h3>My Enrollments</h3>
          {loadingEnrollments ? (
            <p>Loading enrollments...</p>
          ) : enrollments.length === 0 ? (
            <p>No enrollments for this student.</p>
          ) : (
            <table border={1} cellPadding={5}>
              <thead>
                <tr>
                  <th>Course</th>
                  <th>Enrolled At</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                {enrollments.map(e => (
                  <tr key={e.id}>
                    <td>{e.course.title}</td>
                    <td>{new Date(e.enrolled_at).toLocaleString()}</td>
                    <td>
                      <button onClick={() => handleUnenroll(e.id, e.course_id)}>Unenroll</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </>
      )}
    </div>
  );
}