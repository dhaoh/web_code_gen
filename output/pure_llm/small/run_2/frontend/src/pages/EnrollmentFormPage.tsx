import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { enrollmentApi, studentApi, courseApi, Student, Course } from '../api';

const EnrollmentFormPage: React.FC = () => {
  const navigate = useNavigate();

  const [students, setStudents] = useState<Student[]>([]);
  const [courses, setCourses] = useState<Course[]>([]);
  const [selectedStudentId, setSelectedStudentId] = useState<number | ''>('');
  const [selectedCourseId, setSelectedCourseId] = useState<number | ''>('');
  const [errors, setErrors] = useState<{ [key: string]: string }>({});
  const [loading, setLoading] = useState(true);
  const [submitLoading, setSubmitLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);
      const [studentsData, coursesData] = await Promise.all([
        studentApi.getAll(),
        courseApi.getAll(),
      ]);
      setStudents(studentsData);
      setCourses(coursesData);
    } catch (err: any) {
      setError(err.message || 'Failed to load data');
    } finally {
      setLoading(false);
    }
  };

  const validateForm = (): boolean => {
    const newErrors: { [key: string]: string } = {};

    if (!selectedStudentId) {
      newErrors.student = 'Please select a student';
    }

    if (!selectedCourseId) {
      newErrors.course = 'Please select a course';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    try {
      setSubmitLoading(true);
      setError(null);

      await enrollmentApi.create({
        student_id: selectedStudentId as number,
        course_id: selectedCourseId as number,
      });

      navigate('/enrollments');
    } catch (err: any) {
      setError(err.message || 'Failed to create enrollment');
    } finally {
      setSubmitLoading(false);
    }
  };

  if (loading) {
    return <div style={styles.loading}>Loading form data...</div>;
  }

  return (
    <div>
      <h2>New Enrollment</h2>
      
      {error && (
        <div style={styles.error}>
          <p>{error}</p>
        </div>
      )}

      <form onSubmit={handleSubmit} style={styles.form}>
        <div style={styles.formGroup}>
          <label style={styles.label}>Student:</label>
          <select
            value={selectedStudentId}
            onChange={(e) => {
              setSelectedStudentId(e.target.value ? parseInt(e.target.value) : '');
              if (errors.student) {
                setErrors(prev => ({ ...prev, student: '' }));
              }
            }}
            style={{
              ...styles.select,
              ...(errors.student ? styles.inputError : {}),
            }}
          >
            <option value="">Select a student</option>
            {students.map(student => (
              <option key={student.id} value={student.id}>
                {student.name} ({student.email})
              </option>
            ))}
          </select>
          {errors.student && <span style={styles.fieldError}>{errors.student}</span>}
        </div>

        <div style={styles.formGroup}>
          <label style={styles.label}>Course:</label>
          <select
            value={selectedCourseId}
            onChange={(e) => {
              setSelectedCourseId(e.target.value ? parseInt(e.target.value) : '');
              if (errors.course) {
                setErrors(prev => ({ ...prev, course: '' }));
              }
            }}
            style={{
              ...styles.select,
              ...(errors.course ? styles.inputError : {}),
            }}
          >
            <option value="">Select a course</option>
            {courses.map(course => {
              const available = course.capacity - course.enrollment_count;
              return (
                <option key={course.id} value={course.id}>
                  {course.title} (Available: {available}/{course.capacity})
                </option>
              );
            })}
          </select>
          {errors.course && <span style={styles.fieldError}>{errors.course}</span>}
        </div>

        <div style={styles.buttonGroup}>
          <button
            type="submit"
            disabled={submitLoading}
            style={styles.submitButton}
          >
            {submitLoading ? 'Enrolling...' : 'Enroll'}
          </button>
          <button
            type="button"
            onClick={() => navigate('/enrollments')}
            style={styles.cancelButton}
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
};

const styles: { [key: string]: React.CSSProperties } = {
  loading: {
    textAlign: 'center',
    padding: '40px',
    fontSize: '18px',
    color: '#666',
  },
  error: {
    backgroundColor: '#f8d7da',
    color: '#721c24',
    padding: '12px',
    borderRadius: '4px',
    marginBottom: '20px',
  },
  form: {
    maxWidth: '500px',
    margin: '0 auto',
  },
  formGroup: {
    marginBottom: '20px',
  },
  label: {
    display: 'block',
    marginBottom: '5px',
    fontWeight: 'bold',
    color: '#333',
  },
  select: {
    width: '100%',
    padding: '10px',
    border: '1px solid #ced4da',
    borderRadius: '4px',
    fontSize: '16px',
    boxSizing: 'border-box' as const,
    backgroundColor: 'white',
  },
  inputError: {
    borderColor: '#dc3545',
  },
  fieldError: {
    color: '#dc3545',
    fontSize: '14px',
    marginTop: '5px',
    display: 'block',
  },
  buttonGroup: {
    display: 'flex',
    gap: '10px',
    marginTop: '30px',
  },
  submitButton: {
    padding: '10px 20px',
    backgroundColor: '#007bff',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '16px',
    fontWeight: 'bold',
  },
  cancelButton: {
    padding: '10px 20px',
    backgroundColor: '#6c757d',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '16px',
  },
};

export default EnrollmentFormPage;