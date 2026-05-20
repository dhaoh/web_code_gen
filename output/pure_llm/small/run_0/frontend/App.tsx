import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useNavigate, useParams } from 'react-router-dom';
import { studentAPI, courseAPI, enrollmentAPI, Student, Course, Enrollment } from './api';

// Navigation Component
const Navigation: React.FC = () => {
  return (
    <nav style={styles.nav}>
      <div style={styles.navContainer}>
        <Link to="/" style={styles.navBrand}>Student Course System</Link>
        <div style={styles.navLinks}>
          <Link to="/students" style={styles.navLink}>Students</Link>
          <Link to="/courses" style={styles.navLink}>Courses</Link>
          <Link to="/enrollments" style={styles.navLink}>Enrollments</Link>
        </div>
      </div>
    </nav>
  );
};

// Loading Spinner Component
const LoadingSpinner: React.FC = () => (
  <div style={styles.loadingContainer}>
    <div style={styles.loadingSpinner}></div>
    <p>Loading...</p>
  </div>
);

// Error Message Component
const ErrorMessage: React.FC<{ message: string; onRetry?: () => void }> = ({ message, onRetry }) => (
  <div style={styles.errorContainer}>
    <p style={styles.errorText}>Error: {message}</p>
    {onRetry && (
      <button onClick={onRetry} style={styles.retryButton}>
        Retry
      </button>
    )}
  </div>
);

// Empty State Component
const EmptyState: React.FC<{ message: string; actionLabel?: string; onAction?: () => void }> = ({
  message,
  actionLabel,
  onAction,
}) => (
  <div style={styles.emptyContainer}>
    <p style={styles.emptyText}>{message}</p>
    {actionLabel && onAction && (
      <button onClick={onAction} style={styles.actionButton}>
        {actionLabel}
      </button>
    )}
  </div>
);

// Student List Page
const StudentListPage: React.FC = () => {
  const navigate = useNavigate();
  const [students, setStudents] = useState<Student[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchStudents = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await studentAPI.getAll();
      setStudents(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStudents();
  }, []);

  const handleDelete = async (id: number) => {
    if (!window.confirm('Are you sure you want to delete this student?')) return;
    try {
      await studentAPI.delete(id);
      fetchStudents();
    } catch (err: any) {
      setError(err.message);
    }
  };

  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage message={error} onRetry={fetchStudents} />;

  return (
    <div style={styles.pageContainer}>
      <div style={styles.pageHeader}>
        <h1>Students</h1>
        <button onClick={() => navigate('/students/new')} style={styles.addButton}>
          Add Student
        </button>
      </div>
      {students.length === 0 ? (
        <EmptyState
          message="No students found"
          actionLabel="Add your first student"
          onAction={() => navigate('/students/new')}
        />
      ) : (
        <div style={styles.tableContainer}>
          <table style={styles.table}>
            <thead>
              <tr>
                <th style={styles.th}>ID</th>
                <th style={styles.th}>Name</th>
                <th style={styles.th}>Email</th>
                <th style={styles.th}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {students.map((student) => (
                <tr key={student.id}>
                  <td style={styles.td}>{student.id}</td>
                  <td style={styles.td}>{student.name}</td>
                  <td style={styles.td}>{student.email}</td>
                  <td style={styles.td}>
                    <button
                      onClick={() => navigate(`/students/${student.id}/edit`)}
                      style={styles.editButton}
                    >
                      Edit
                    </button>
                    <button
                      onClick={() => handleDelete(student.id)}
                      style={styles.deleteButton}
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

// Student Form Page (Create/Edit)
const StudentFormPage: React.FC = () => {
  const navigate = useNavigate();
  const { id } = useParams<{ id: string }>();
  const isEdit = Boolean(id);
  const [formData, setFormData] = useState({ name: '', email: '' });
  const [errors, setErrors] = useState<{ name?: string; email?: string }>({});
  const [loading, setLoading] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);

  useEffect(() => {
    if (isEdit && id) {
      const fetchStudent = async () => {
        try {
          setLoading(true);
          const student = await studentAPI.getById(parseInt(id));
          setFormData({ name: student.name, email: student.email });
        } catch (err: any) {
          setSubmitError(err.message);
        } finally {
          setLoading(false);
        }
      };
      fetchStudent();
    }
  }, [id, isEdit]);

  const validate = (): boolean => {
    const newErrors: { name?: string; email?: string } = {};
    if (!formData.name.trim()) {
      newErrors.name = 'Name is required';
    }
    if (!formData.email.trim()) {
      newErrors.email = 'Email is required';
    } else if (!formData.email.includes('@') || !formData.email.includes('.')) {
      newErrors.email = 'Invalid email format';
    }
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validate()) return;

    try {
      setLoading(true);
      setSubmitError(null);
      if (isEdit && id) {
        await studentAPI.update(parseInt(id), formData);
      } else {
        await studentAPI.create(formData);
      }
      navigate('/students');
    } catch (err: any) {
      setSubmitError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    setErrors({ ...errors, [e.target.name]: undefined });
  };

  if (loading && isEdit) return <LoadingSpinner />;

  return (
    <div style={styles.pageContainer}>
      <h1>{isEdit ? 'Edit Student' : 'Add Student'}</h1>
      {submitError && <ErrorMessage message={submitError} />}
      <form onSubmit={handleSubmit} style={styles.form}>
        <div style={styles.formGroup}>
          <label style={styles.label}>Name:</label>
          <input
            type="text"
            name="name"
            value={formData.name}
            onChange={handleChange}
            style={styles.input}
          />
          {errors.name && <span style={styles.fieldError}>{errors.name}</span>}
        </div>
        <div style={styles.formGroup}>
          <label style={styles.label}>Email:</label>
          <input
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            style={styles.input}
          />
          {errors.email && <span style={styles.fieldError}>{errors.email}</span>}
        </div>
        <div style={styles.formActions}>
          <button type="submit" disabled={loading} style={styles.submitButton}>
            {loading ? 'Saving...' : isEdit ? 'Update' : 'Create'}
          </button>
          <button type="button" onClick={() => navigate('/students')} style={styles.cancelButton}>
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
};

// Course List Page
const CourseListPage: React.FC = () => {
  const navigate = useNavigate();
  const [courses, setCourses] = useState<Course[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchCourses = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await courseAPI.getAll();
      setCourses(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCourses();
  }, []);

  const handleDelete = async (id: number) => {
    if (!window.confirm('Are you sure you want to delete this course?')) return;
    try {
      await courseAPI.delete(id);
      fetchCourses();
    } catch (err: any) {
      setError(err.message);
    }
  };

  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage message={error} onRetry={fetchCourses} />;

  return (
    <div style={styles.pageContainer}>
      <div style={styles.pageHeader}>
        <h1>Courses</h1>
        <button onClick={() => navigate('/courses/new')} style={styles.addButton}>
          Add Course
        </button>
      </div>
      {courses.length === 0 ? (
        <EmptyState
          message="No courses found"
          actionLabel="Add your first course"
          onAction={() => navigate('/courses/new')}
        />
      ) : (
        <div style={styles.tableContainer}>
          <table style={styles.table}>
            <thead>
              <tr>
                <th style={styles.th}>ID</th>
                <th style={styles.th}>Title</th>
                <th style={styles.th}>Capacity</th>
                <th style={styles.th}>Enrolled</th>
                <th style={styles.th}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {courses.map((course) => (
                <tr key={course.id}>
                  <td style={styles.td}>{course.id}</td>
                  <td style={styles.td}>{course.title}</td>
                  <td style={styles.td}>{course.capacity}</td>
                  <td style={styles.td}>{course.enrolled_count || 0}</td>
                  <td style={styles.td}>
                    <button
                      onClick={() => navigate(`/courses/${course.id}/edit`)}
                      style={styles.editButton}
                    >
                      Edit
                    </button>
                    <button
                      onClick={() => handleDelete(course.id)}
                      style={styles.deleteButton}
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

// Course Form Page (Create/Edit)
const CourseFormPage: React.FC = () => {
  const navigate = useNavigate();
  const { id } = useParams<{ id: string }>();
  const isEdit = Boolean(id);
  const [formData, setFormData] = useState({ title: '', description: '', capacity: '' });
  const [errors, setErrors] = useState<{ title?: string; capacity?: string }>({});
  const [loading, setLoading] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);

  useEffect(() => {
    if (isEdit && id) {
      const fetchCourse = async () => {
        try {
          setLoading(true);
          const course = await courseAPI.getById(parseInt(id));
          setFormData({
            title: course.title,
            description: course.description || '',
            capacity: course.capacity.toString(),
          });
        } catch (err: any) {
          setSubmitError(err.message);
        } finally {
          setLoading(false);
        }
      };
      fetchCourse();
    }
  }, [id, isEdit]);

  const validate = (): boolean => {
    const newErrors: { title?: string; capacity?: string } = {};
    if (!formData.title.trim()) {
      newErrors.title = 'Title is required';
    }
    if (!formData.capacity.trim()) {
      newErrors.capacity = 'Capacity is required';
    } else if (parseInt(formData.capacity) < 1) {
      newErrors.capacity = 'Capacity must be at least 1';
    }
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validate()) return;

    try {
      setLoading(true);
      setSubmitError(null);
      const data = {
        title: formData.title,
        description: formData.description || undefined,
        capacity: parseInt(formData.capacity),
      };
      if (isEdit && id) {
        await courseAPI.update(parseInt(id), data);
      } else {
        await courseAPI.create(data);
      }
      navigate('/courses');
    } catch (err: any) {
      setSubmitError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    setErrors({ ...errors, [e.target.name]: undefined });
  };

  if (loading && isEdit) return <LoadingSpinner />;

  return (
    <div style={styles.pageContainer}>
      <h1>{isEdit ? 'Edit Course' : 'Add Course'}</h1>
      {submitError && <ErrorMessage message={submitError} />}
      <form onSubmit={handleSubmit} style={styles.form}>
        <div style={styles.formGroup}>
          <label style={styles.label}>Title:</label>
          <input
            type="text"
            name="title"
            value={formData.title}
            onChange={handleChange}
            style={styles.input}
          />
          {errors.title && <span style={styles.fieldError}>{errors.title}</span>}
        </div>
        <div style={styles.formGroup}>
          <label style={styles.label}>Description:</label>
          <textarea
            name="description"
            value={formData.description}
            onChange={handleChange}
            style={styles.textarea}
          />
        </div>
        <div style={styles.formGroup}>
          <label style={styles.label}>Capacity:</label>
          <input
            type="number"
            name="capacity"
            value={formData.capacity}
            onChange={handleChange}
            min="1"
            style={styles.input}
          />
          {errors.capacity && <span style={styles.fieldError}>{errors.capacity}</span>}
        </div>
        <div style={styles.formActions}>
          <button type="submit" disabled={loading} style={styles.submitButton}>
            {loading ? 'Saving...' : isEdit ? 'Update' : 'Create'}
          </button>
          <button type="button" onClick={() => navigate('/courses')} style={styles.cancelButton}>
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
};

// Enrollment List Page
const EnrollmentListPage: React.FC = () => {
  const navigate = useNavigate();
  const [enrollments, setEnrollments] = useState<Enrollment[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchEnrollments = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await enrollmentAPI.getAll();
      setEnrollments(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchEnrollments();
  }, []);

  const handleDelete = async (id: number) => {
    if (!window.confirm('Are you sure you want to delete this enrollment?')) return;
    try {
      await enrollmentAPI.delete(id);
      fetchEnrollments();
    } catch (err: any) {
      setError(err.message);
    }
  };

  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage message={error} onRetry={fetchEnrollments} />;

  return (
    <div style={styles.pageContainer}>
      <div style={styles.pageHeader}>
        <h1>Enrollments</h1>
        <button onClick={() => navigate('/enrollments/new')} style={styles.addButton}>
          New Enrollment
        </button>
      </div>
      {enrollments.length === 0 ? (
        <EmptyState
          message="No enrollments found"
          actionLabel="Create your first enrollment"
          onAction={() => navigate('/enrollments/new')}
        />
      ) : (
        <div style={styles.tableContainer}>
          <table style={styles.table}>
            <thead>
              <tr>
                <th style={styles.th}>ID</th>
                <th style={styles.th}>Student</th>
                <th style={styles.th}>Course</th>
                <th style={styles.th}>Enrolled At</th>
                <th style={styles.th}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {enrollments.map((enrollment) => (
                <tr key={enrollment.id}>
                  <td style={styles.td}>{enrollment.id}</td>
                  <td style={styles.td}>
                    {enrollment.student ? enrollment.student.name : `Student #${enrollment.student_id}`}
                  </td>
                  <td style={styles.td}>
                    {enrollment.course ? enrollment.course.title : `Course #${enrollment.course_id}`}
                  </td>
                  <td style={styles.td}>{new Date(enrollment.enrolled_at).toLocaleString()}</td>
                  <td style={styles.td}>
                    <button
                      onClick={() => handleDelete(enrollment.id)}
                      style={styles.deleteButton}
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

// Enrollment Form Page
const EnrollmentFormPage: React.FC = () => {
  const navigate = useNavigate();
  const [students, setStudents] = useState<Student[]>([]);
  const [courses, setCourses] = useState<Course[]>([]);
  const [formData, setFormData] = useState({ student_id: '', course_id: '' });
  const [errors, setErrors] = useState<{ student_id?: string; course_id?: string }>({});
  const [loading, setLoading] = useState(true);
  const [submitError, setSubmitError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const [studentsData, coursesData] = await Promise.all([
          studentAPI.getAll(),
          courseAPI.getAll(),
        ]);
        setStudents(studentsData);
        setCourses(coursesData);
      } catch (err: any) {
        setSubmitError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const validate = (): boolean => {
    const newErrors: { student_id?: string; course_id?: string } = {};
    if (!formData.student_id) {
      newErrors.student_id = 'Please select a student';
    }
    if (!formData.course_id) {
      newErrors.course_id = 'Please select a course';
    }
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validate()) return;

    try {
      setLoading(true);
      setSubmitError(null);
      await enrollmentAPI.create({
        student_id: parseInt(formData.student_id),
        course_id: parseInt(formData.course_id),
      });
      navigate('/enrollments');
    } catch (err: any) {
      setSubmitError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    setErrors({ ...errors, [e.target.name]: undefined });
  };

  if (loading) return <LoadingSpinner />;

  return (
    <div style={styles.pageContainer}>
      <h1>New Enrollment</h1>
      {submitError && <ErrorMessage message={submitError} />}
      <form onSubmit={handleSubmit} style={styles.form}>
        <div style={styles.formGroup}>
          <label style={styles.label}>Student:</label>
          <select
            name="student_id"
            value={formData.student_id}
            onChange={handleChange}
            style={styles.select}
          >
            <option value="">Select a student</option>
            {students.map((student) => (
              <option key={student.id} value={student.id}>
                {student.name} ({student.email})
              </option>
            ))}
          </select>
          {errors.student_id && <span style={styles.fieldError}>{errors.student_id}</span>}
        </div>
        <div style={styles.formGroup}>
          <label style={styles.label}>Course:</label>
          <select
            name="course_id"
            value={formData.course_id}
            onChange={handleChange}
            style={styles.select}
          >
            <option value="">Select a course</option>
            {courses.map((course) => (
              <option key={course.id} value={course.id}>
                {course.title} ({course.enrolled_count || 0}/{course.capacity})
              </option>
            ))}
          </select>
          {errors.course_id && <span style={styles.fieldError}>{errors.course_id}</span>}
        </div>
        <div style={styles.formActions}>
          <button type="submit" disabled={loading} style={styles.submitButton}>
            {loading ? 'Enrolling...' : 'Enroll'}
          </button>
          <button type="button" onClick={() => navigate('/enrollments')} style={styles.cancelButton}>
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
};

// Home Page
const HomePage: React.FC = () => {
  return (
    <div style={styles.pageContainer}>
      <h1>Welcome to Student Course System</h1>
      <p style={styles.homeText}>
        Manage students, courses, and enrollments in one place.
      </p>
      <div style={styles.homeLinks}>
        <Link to="/students" style={styles.homeLink}>
          <h3>Students</h3>
          <p>View and manage student records</p>
        </Link>
        <Link to="/courses" style={styles.homeLink}>
          <h3>Courses</h3>
          <p>Browse and manage available courses</p>
        </Link>
        <Link to="/enrollments" style={styles.homeLink}>
          <h3>Enrollments</h3>
          <p>Track student course enrollments</p>
        </Link>
      </div>
    </div>
  );
};

// Main App Component
const App: React.FC = () => {
  return (
    <Router>
      <div style={styles.app}>
        <Navigation />
        <main style={styles.main}>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/students" element={<StudentListPage />} />
            <Route path="/students/new" element={<StudentFormPage />} />
            <Route path="/students/:id/edit" element={<StudentFormPage />} />
            <Route path="/courses" element={<CourseListPage />} />
            <Route path="/courses/new" element={<CourseFormPage />} />
            <Route path="/courses/:id/edit" element={<CourseFormPage />} />
            <Route path="/enrollments" element={<EnrollmentListPage />} />
            <Route path="/enrollments/new" element={<EnrollmentFormPage />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
};

// Styles
const styles: Record<string, React.CSSProperties> = {
  app: {
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, sans-serif',
    minHeight: '100vh',
    backgroundColor: '#f5f5f5',
  },
  nav: {
    backgroundColor: '#1976d2',
    padding: '1rem 0',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
  },
  navContainer: {
    maxWidth: '1200px',
    margin: '0 auto',
    padding: '0 1rem',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  navBrand: {
    color: 'white',
    textDecoration: 'none',
    fontSize: '1.5rem',
    fontWeight: 'bold',
  },
  navLinks: {
    display: 'flex',
    gap: '1rem',
  },
  navLink: {
    color: 'white',
    textDecoration: 'none',
    padding: '0.5rem 1rem',
    borderRadius: '4px',
    transition: 'background-color 0.3s',
  },
  main: {
    maxWidth: '1200px',
    margin: '2rem auto',
    padding: '0 1rem',
  },
  pageContainer: {
    backgroundColor: 'white',
    borderRadius: '8px',
    padding: '2rem',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
  },
  pageHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '1.5rem',
  },
  tableContainer: {
    overflowX: 'auto',
  },
  table: {
    width: '100%',
    borderCollapse: 'collapse',
  },
  th: {
    backgroundColor: '#f5f5f5',
    padding: '0.75rem',
    textAlign: 'left',
    borderBottom: '2px solid #ddd',
    fontWeight: 'bold',
  },
  td: {
    padding: '0.75rem',
    borderBottom: '1px solid #ddd',
  },
  addButton: {
    backgroundColor: '#1976d2',
    color: 'white',
    border: 'none',
    padding: '0.5rem 1rem',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '1rem',
  },
  editButton: {
    backgroundColor: '#ff9800',
    color: 'white',
    border: 'none',
    padding: '0.25rem 0.5rem',
    borderRadius: '4px',
    cursor: 'pointer',
    marginRight: '0.5rem',
  },
  deleteButton: {
    backgroundColor: '#f44336',
    color: 'white',
    border: 'none',
    padding: '0.25rem 0.5rem',
    borderRadius: '4px',
    cursor: 'pointer',
  },
  form: {
    maxWidth: '500px',
    margin: '0 auto',
  },
  formGroup: {
    marginBottom: '1rem',
  },
  label: {
    display: 'block',
    marginBottom: '0.5rem',
    fontWeight: 'bold',
  },
  input: {
    width: '100%',
    padding: '0.5rem',
    border: '1px solid #ddd',
    borderRadius: '4px',
    fontSize: '1rem',
  },
  textarea: {
    width: '100%',
    padding: '0.5rem',
    border: '1px solid #ddd',
    borderRadius: '4px',
    fontSize: '1rem',
    minHeight: '100px',
    resize: 'vertical',
  },
  select: {
    width: '100%',
    padding: '0.5rem',
    border: '1px solid #ddd',
    borderRadius: '4px',
    fontSize: '1rem',
    backgroundColor: 'white',
  },
  formActions: {
    display: 'flex',
    gap: '1rem',
    marginTop: '1.5rem',
  },
  submitButton: {
    backgroundColor: '#1976d2',
    color: 'white',
    border: 'none',
    padding: '0.5rem 1rem',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '1rem',
  },
  cancelButton: {
    backgroundColor: '#9e9e9e',
    color: 'white',
    border: 'none',
    padding: '0.5rem 1rem',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '1rem',
  },
  fieldError: {
    color: '#f44336',
    fontSize: '0.875rem',
    marginTop: '0.25rem',
    display: 'block',
  },
  loadingContainer: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    padding: '3rem',
  },
  loadingSpinner: {
    border: '4px solid #f3f3f3',
    borderTop: '4px solid #1976d2',
    borderRadius: '50%',
    width: '40px',
    height: '40px',
    animation: 'spin 1s linear infinite',
    marginBottom: '1rem',
  },
  errorContainer: {
    backgroundColor: '#ffebee',
    border: '1px solid #f44336',
    borderRadius: '4px',
    padding: '1rem',
    marginBottom: '1rem',
  },
  errorText: {
    color: '#f44336',
    margin: '0 0 0.5rem 0',
  },
  retryButton: {
    backgroundColor: '#f44336',
    color: 'white',
    border: 'none',
    padding: '0.25rem 0.5rem',
    borderRadius: '4px',
    cursor: 'pointer',
  },
  emptyContainer: {
    textAlign: 'center',
    padding: '3rem',
  },
  emptyText: {
    color: '#666',
    fontSize: '1.1rem',
    marginBottom: '1rem',
  },
  actionButton: {
    backgroundColor: '#1976d2',
    color: 'white',
    border: 'none',
    padding: '0.5rem 1rem',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '1rem',
  },
  homeText: {
    fontSize: '1.2rem',
    color: '#666',
    marginBottom: '2rem',
  },
  homeLinks: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
    gap: '1.5rem',
  },
  homeLink: {
    backgroundColor: '#f5f5f5',
    padding: '1.5rem',
    borderRadius: '8px',
    textDecoration: 'none',
    color: '#333',
    transition: 'transform 0.2s, box-shadow 0.2s',
    display: 'block',
  },
};

export default App;