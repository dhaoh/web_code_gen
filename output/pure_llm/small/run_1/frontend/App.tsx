import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom/client';
import './styles.css';

// Import API functions
import {
  Student, StudentCreate, StudentUpdate,
  Course, CourseCreate, CourseUpdate,
  Enrollment, EnrollmentCreate,
  getStudents, getStudent, createStudent, updateStudent, deleteStudent,
  getCourses, getCourse, createCourse, updateCourse, deleteCourse,
  getEnrollments, createEnrollment, deleteEnrollment,
  getStudentEnrollments, getCourseEnrollments
} from './api';

// Navigation component
function Navigation({ currentPage, setCurrentPage }: { currentPage: string; setCurrentPage: (page: string) => void }) {
  return (
    <nav className="navigation">
      <button
        className={currentPage === 'students' ? 'active' : ''}
        onClick={() => setCurrentPage('students')}
      >
        Students
      </button>
      <button
        className={currentPage === 'courses' ? 'active' : ''}
        onClick={() => setCurrentPage('courses')}
      >
        Courses
      </button>
      <button
        className={currentPage === 'enrollments' ? 'active' : ''}
        onClick={() => setCurrentPage('enrollments')}
      >
        Enrollments
      </button>
    </nav>
  );
}

// Student List Page
function StudentListPage({ onEdit }: { onEdit: (id: number) => void }) {
  const [students, setStudents] = useState<Student[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchStudents = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await getStudents();
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
      await deleteStudent(id);
      fetchStudents();
    } catch (err: any) {
      alert(err.message);
    }
  };

  if (loading) return <div className="loading">Loading students...</div>;
  if (error) return <div className="error">Error: {error}</div>;
  if (students.length === 0) return <div className="empty">No students found. Create one!</div>;

  return (
    <div className="list-page">
      <div className="page-header">
        <h2>Students</h2>
        <button className="btn-primary" onClick={() => onEdit(0)}>Add Student</button>
      </div>
      <table className="data-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Email</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {students.map(student => (
            <tr key={student.id}>
              <td>{student.id}</td>
              <td>{student.name}</td>
              <td>{student.email}</td>
              <td>
                <button className="btn-secondary" onClick={() => onEdit(student.id)}>Edit</button>
                <button className="btn-danger" onClick={() => handleDelete(student.id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

// Student Form Page
function StudentFormPage({ studentId, onBack }: { studentId: number; onBack: () => void }) {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [validationErrors, setValidationErrors] = useState<{ [key: string]: string }>({});

  useEffect(() => {
    if (studentId) {
      fetchStudent();
    }
  }, [studentId]);

  const fetchStudent = async () => {
    try {
      setLoading(true);
      const student = await getStudent(studentId);
      setName(student.name);
      setEmail(student.email);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const validate = (): boolean => {
    const errors: { [key: string]: string } = {};
    if (!name.trim()) errors.name = 'Name is required';
    if (!email.trim()) errors.email = 'Email is required';
    else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) errors.email = 'Invalid email format';
    setValidationErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validate()) return;

    try {
      setLoading(true);
      setError(null);
      if (studentId) {
        await updateStudent(studentId, { name, email });
      } else {
        await createStudent({ name, email });
      }
      onBack();
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="form-page">
      <div className="page-header">
        <h2>{studentId ? 'Edit Student' : 'Add Student'}</h2>
        <button className="btn-secondary" onClick={onBack}>Back</button>
      </div>
      {error && <div className="error">{error}</div>}
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="name">Name:</label>
          <input
            id="name"
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            className={validationErrors.name ? 'error' : ''}
          />
          {validationErrors.name && <span className="validation-error">{validationErrors.name}</span>}
        </div>
        <div className="form-group">
          <label htmlFor="email">Email:</label>
          <input
            id="email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className={validationErrors.email ? 'error' : ''}
          />
          {validationErrors.email && <span className="validation-error">{validationErrors.email}</span>}
        </div>
        <button type="submit" className="btn-primary" disabled={loading}>
          {loading ? 'Saving...' : 'Save'}
        </button>
      </form>
    </div>
  );
}

// Course List Page
function CourseListPage({ onEdit }: { onEdit: (id: number) => void }) {
  const [courses, setCourses] = useState<Course[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchCourses = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await getCourses();
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
      await deleteCourse(id);
      fetchCourses();
    } catch (err: any) {
      alert(err.message);
    }
  };

  if (loading) return <div className="loading">Loading courses...</div>;
  if (error) return <div className="error">Error: {error}</div>;
  if (courses.length === 0) return <div className="empty">No courses found. Create one!</div>;

  return (
    <div className="list-page">
      <div className="page-header">
        <h2>Courses</h2>
        <button className="btn-primary" onClick={() => onEdit(0)}>Add Course</button>
      </div>
      <table className="data-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Title</th>
            <th>Description</th>
            <th>Capacity</th>
            <th>Enrolled</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {courses.map(course => (
            <tr key={course.id}>
              <td>{course.id}</td>
              <td>{course.title}</td>
              <td>{course.description || '-'}</td>
              <td>{course.capacity}</td>
              <td>{course.enrolled_count}</td>
              <td>
                <button className="btn-secondary" onClick={() => onEdit(course.id)}>Edit</button>
                <button className="btn-danger" onClick={() => handleDelete(course.id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

// Course Form Page
function CourseFormPage({ courseId, onBack }: { courseId: number; onBack: () => void }) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [capacity, setCapacity] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [validationErrors, setValidationErrors] = useState<{ [key: string]: string }>({});

  useEffect(() => {
    if (courseId) {
      fetchCourse();
    }
  }, [courseId]);

  const fetchCourse = async () => {
    try {
      setLoading(true);
      const course = await getCourse(courseId);
      setTitle(course.title);
      setDescription(course.description || '');
      setCapacity(course.capacity.toString());
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const validate = (): boolean => {
    const errors: { [key: string]: string } = {};
    if (!title.trim()) errors.title = 'Title is required';
    if (!capacity.trim()) errors.capacity = 'Capacity is required';
    else {
      const cap = parseInt(capacity);
      if (isNaN(cap) || cap <= 0) errors.capacity = 'Capacity must be a positive number';
      else if (cap > 1000) errors.capacity = 'Capacity cannot exceed 1000';
    }
    setValidationErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validate()) return;

    try {
      setLoading(true);
      setError(null);
      const courseData: CourseCreate | CourseUpdate = {
        title,
        description: description || undefined,
        capacity: parseInt(capacity),
      };
      if (courseId) {
        await updateCourse(courseId, courseData);
      } else {
        await createCourse(courseData as CourseCreate);
      }
      onBack();
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="form-page">
      <div className="page-header">
        <h2>{courseId ? 'Edit Course' : 'Add Course'}</h2>
        <button className="btn-secondary" onClick={onBack}>Back</button>
      </div>
      {error && <div className="error">{error}</div>}
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="title">Title:</label>
          <input
            id="title"
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className={validationErrors.title ? 'error' : ''}
          />
          {validationErrors.title && <span className="validation-error">{validationErrors.title}</span>}
        </div>
        <div className="form-group">
          <label htmlFor="description">Description:</label>
          <textarea
            id="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
          />
        </div>
        <div className="form-group">
          <label htmlFor="capacity">Capacity:</label>
          <input
            id="capacity"
            type="number"
            value={capacity}
            onChange={(e) => setCapacity(e.target.value)}
            className={validationErrors.capacity ? 'error' : ''}
          />
          {validationErrors.capacity && <span className="validation-error">{validationErrors.capacity}</span>}
        </div>
        <button type="submit" className="btn-primary" disabled={loading}>
          {loading ? 'Saving...' : 'Save'}
        </button>
      </form>
    </div>
  );
}

// Enrollment List Page
function EnrollmentListPage() {
  const [enrollments, setEnrollments] = useState<Enrollment[]>([]);
  const [students, setStudents] = useState<Student[]>([]);
  const [courses, setCourses] = useState<Course[]>([]);
  const [selectedStudent, setSelectedStudent] = useState('');
  const [selectedCourse, setSelectedCourse] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showForm, setShowForm] = useState(false);

  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);
      const [enrollmentsData, studentsData, coursesData] = await Promise.all([
        getEnrollments(),
        getStudents(),
        getCourses()
      ]);
      setEnrollments(enrollmentsData);
      setStudents(studentsData);
      setCourses(coursesData);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleEnroll = async () => {
    if (!selectedStudent || !selectedCourse) {
      alert('Please select both a student and a course');
      return;
    }

    try {
      const enrollmentData: EnrollmentCreate = {
        student_id: parseInt(selectedStudent),
        course_id: parseInt(selectedCourse),
      };
      await createEnrollment(enrollmentData);
      setShowForm(false);
      setSelectedStudent('');
      setSelectedCourse('');
      fetchData();
    } catch (err: any) {
      alert(err.message);
    }
  };

  const handleDelete = async (id: number) => {
    if (!window.confirm('Are you sure you want to delete this enrollment?')) return;
    try {
      await deleteEnrollment(id);
      fetchData();
    } catch (err: any) {
      alert(err.message);
    }
  };

  if (loading) return <div className="loading">Loading enrollments...</div>;
  if (error) return <div className="error">Error: {error}</div>;

  return (
    <div className="list-page">
      <div className="page-header">
        <h2>Enrollments</h2>
        <button className="btn-primary" onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Cancel' : 'New Enrollment'}
        </button>
      </div>

      {showForm && (
        <div className="enrollment-form">
          <h3>Create Enrollment</h3>
          <div className="form-group">
            <label>Student:</label>
            <select value={selectedStudent} onChange={(e) => setSelectedStudent(e.target.value)}>
              <option value="">Select a student</option>
              {students.map(student => (
                <option key={student.id} value={student.id}>{student.name} ({student.email})</option>
              ))}
            </select>
          </div>
          <div className="form-group">
            <label>Course:</label>
            <select value={selectedCourse} onChange={(e) => setSelectedCourse(e.target.value)}>
              <option value="">Select a course</option>
              {courses.map(course => (
                <option key={course.id} value={course.id}>
                  {course.title} ({course.enrolled_count}/{course.capacity})
                </option>
              ))}
            </select>
          </div>
          <button className="btn-primary" onClick={handleEnroll}>Enroll</button>
        </div>
      )}

      {enrollments.length === 0 ? (
        <div className="empty">No enrollments found.</div>
      ) : (
        <table className="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Student</th>
              <th>Course</th>
              <th>Enrolled At</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {enrollments.map(enrollment => (
              <tr key={enrollment.id}>
                <td>{enrollment.id}</td>
                <td>{enrollment.student_name}</td>
                <td>{enrollment.course_title}</td>
                <td>{new Date(enrollment.enrolled_at).toLocaleString()}</td>
                <td>
                  <button className="btn-danger" onClick={() => handleDelete(enrollment.id)}>Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

// Main App Component
function App() {
  const [currentPage, setCurrentPage] = useState('students');
  const [editId, setEditId] = useState<number | null>(null);

  const handleEdit = (id: number) => {
    setEditId(id);
  };

  const handleBack = () => {
    setEditId(null);
  };

  const renderPage = () => {
    if (editId !== null) {
      if (currentPage === 'students') {
        return <StudentFormPage studentId={editId} onBack={handleBack} />;
      }
      if (currentPage === 'courses') {
        return <CourseFormPage courseId={editId} onBack={handleBack} />;
      }
    }

    switch (currentPage) {
      case 'students':
        return <StudentListPage onEdit={handleEdit} />;
      case 'courses':
        return <CourseListPage onEdit={handleEdit} />;
      case 'enrollments':
        return <EnrollmentListPage />;
      default:
        return <StudentListPage onEdit={handleEdit} />;
    }
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>Student Course System</h1>
        <Navigation currentPage={currentPage} setCurrentPage={(page) => {
          setCurrentPage(page);
          setEditId(null);
        }} />
      </header>
      <main className="app-content">
        {renderPage()}
      </main>
    </div>
  );
}

// Mount the app
const root = ReactDOM.createRoot(document.getElementById('root')!);
root.render(<App />);