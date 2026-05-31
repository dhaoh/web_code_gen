from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import User, Department, Course, Enrollment, Grade, Assignment
from schemas import (
    UserCreate, UserLogin, UserUpdate, UserResponse,
    DepartmentCreate, DepartmentUpdate, DepartmentResponse,
    CourseCreate, CourseUpdate, CourseResponse,
    EnrollmentCreate, EnrollmentResponse,
    GradeCreate, GradeUpdate, GradeResponse,
    AssignmentCreate, AssignmentUpdate, AssignmentResponse
)
from auth import (
    get_password_hash, verify_password, create_access_token,
    get_current_user
)
import logging

router = APIRouter()

def compute_letter_grade(score: float) -> str:
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"

# ------------------- Auth -------------------
@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter((User.username == user.username) | (User.email == user.email)).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username or email already exists")
    hashed = get_password_hash(user.password)
    new_user = User(
        username=user.username,
        password_hash=hashed,
        role=user.role,
        full_name=user.full_name,
        email=user.email
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login")
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == credentials.username).first()
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/users/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

# ------------------- Users (admin/teacher management) -------------------
@router.get("/users", response_model=List[UserResponse])
def get_users(
    role: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can view all users")
    query = db.query(User)
    if role:
        query = query.filter(User.role == role)
    return query.all()

@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "teacher" and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/users/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "teacher" and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user_update.role and current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can change roles")
    update_data = user_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can delete users")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return

# ------------------- Departments -------------------
@router.get("/departments", response_model=List[DepartmentResponse])
def list_departments(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Department).all()

@router.post("/departments", response_model=DepartmentResponse, status_code=status.HTTP_201_CREATED)
def create_department(
    dept: DepartmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can manage departments")
    exists = db.query(Department).filter(
        (Department.name == dept.name) | (Department.code == dept.code)
    ).first()
    if exists:
        raise HTTPException(status_code=400, detail="Department name or code already exists")
    new_dept = Department(name=dept.name, code=dept.code)
    db.add(new_dept)
    db.commit()
    db.refresh(new_dept)
    return new_dept

@router.get("/departments/{dept_id}", response_model=DepartmentResponse)
def get_department(dept_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    dept = db.query(Department).filter(Department.id == dept_id).first()
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")
    return dept

@router.put("/departments/{dept_id}", response_model=DepartmentResponse)
def update_department(
    dept_id: int,
    dept_update: DepartmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can manage departments")
    dept = db.query(Department).filter(Department.id == dept_id).first()
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")
    # Check uniqueness
    if dept_update.name != dept.name or dept_update.code != dept.code:
        conflict = db.query(Department).filter(
            (Department.id != dept_id) &
            ((Department.name == dept_update.name) | (Department.code == dept_update.code))
        ).first()
        if conflict:
            raise HTTPException(status_code=400, detail="Name or code already in use")
    update_data = dept_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(dept, key, value)
    db.commit()
    db.refresh(dept)
    return dept

@router.delete("/departments/{dept_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_department(
    dept_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can manage departments")
    dept = db.query(Department).filter(Department.id == dept_id).first()
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")
    db.delete(dept)
    db.commit()
    return

# ------------------- Courses -------------------
@router.get("/courses", response_model=List[CourseResponse])
def list_courses(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    courses = db.query(Course).all()
    # optionally eager load relationships
    return courses

@router.post("/courses", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
def create_course(
    course: CourseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can create courses")
    # Check teacher_id points to a teacher
    teacher = db.query(User).filter(User.id == course.teacher_id, User.role == "teacher").first()
    if not teacher:
        raise HTTPException(status_code=400, detail="Invalid teacher_id or user is not a teacher")
    # Check department exists
    dept = db.query(Department).filter(Department.id == course.department_id).first()
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")
    new_course = Course(**course.dict())
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course

@router.get("/courses/{course_id}", response_model=CourseResponse)
def get_course(course_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.put("/courses/{course_id}", response_model=CourseResponse)
def update_course(
    course_id: int,
    course_update: CourseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can update courses")
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    # check teacher/department if provided
    if course_update.teacher_id is not None:
        teacher = db.query(User).filter(User.id == course_update.teacher_id, User.role == "teacher").first()
        if not teacher:
            raise HTTPException(status_code=400, detail="Invalid teacher_id or user is not a teacher")
    if course_update.department_id is not None:
        dept = db.query(Department).filter(Department.id == course_update.department_id).first()
        if not dept:
            raise HTTPException(status_code=404, detail="Department not found")
    update_data = course_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(course, key, value)
    db.commit()
    db.refresh(course)
    return course

@router.delete("/courses/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can delete courses")
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    db.delete(course)
    db.commit()
    return

# ------------------- Enrollments -------------------
@router.get("/enrollments", response_model=List[EnrollmentResponse])
def list_enrollments(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role == "student":
        enrollments = db.query(Enrollment).filter(Enrollment.student_id == current_user.id).all()
    elif current_user.role == "teacher":
        # enrollments for courses taught by this teacher
        enrollments = db.query(Enrollment).join(Course).filter(Course.teacher_id == current_user.id).all()
    else:
        raise HTTPException(status_code=403, detail="Invalid role")
    return enrollments

@router.post("/enrollments", response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED)
def create_enrollment(
    enrollment: EnrollmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "student":
        raise HTTPException(status_code=403, detail="Only students can enroll")

    course = db.query(Course).filter(Course.id == enrollment.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # Check duplicate enrollment
    existing = db.query(Enrollment).filter(
        Enrollment.student_id == current_user.id,
        Enrollment.course_id == enrollment.course_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already enrolled in this course")

    # Check capacity
    enrollment_count = db.query(Enrollment).filter(Enrollment.course_id == enrollment.course_id).count()
    if enrollment_count >= course.capacity:
        raise HTTPException(status_code=400, detail="Course is full")

    # Credit limit check (total credits across all enrollments)
    total_credits = 0
    student_enrollments = db.query(Enrollment).filter(Enrollment.student_id == current_user.id).all()
    for enr in student_enrollments:
        total_credits += enr.course.credits
    total_credits += course.credits
    if total_credits > 30:
        raise HTTPException(status_code=400, detail="Enrolling would exceed 30 credit limit")

    new_enrollment = Enrollment(student_id=current_user.id, course_id=enrollment.course_id)
    db.add(new_enrollment)
    db.commit()
    db.refresh(new_enrollment)
    return new_enrollment

@router.get("/enrollments/{enrollment_id}", response_model=EnrollmentResponse)
def get_enrollment(
    enrollment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    enrollment = db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    if current_user.role == "student" and enrollment.student_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    if current_user.role == "teacher" and enrollment.course.teacher_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    return enrollment

@router.delete("/enrollments/{enrollment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_enrollment(
    enrollment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    enrollment = db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    if current_user.role == "student" and enrollment.student_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only drop your own enrollments")
    if current_user.role == "teacher" and enrollment.course.teacher_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    db.delete(enrollment)
    db.commit()
    return

# ------------------- Grades -------------------
@router.get("/grades", response_model=List[GradeResponse])
def list_grades(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role == "student":
        grades = db.query(Grade).join(Enrollment).filter(Enrollment.student_id == current_user.id).all()
    elif current_user.role == "teacher":
        grades = db.query(Grade).join(Enrollment).join(Course).filter(Course.teacher_id == current_user.id).all()
    else:
        raise HTTPException(status_code=403, detail="Invalid role")
    return grades

@router.post("/grades", response_model=GradeResponse, status_code=status.HTTP_201_CREATED)
def create_grade(
    grade: GradeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can assign grades")

    enrollment = db.query(Enrollment).filter(Enrollment.id == grade.enrollment_id).first()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")

    # Check that this teacher is the instructor of the course
    if enrollment.course.teacher_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only grade your own courses")

    # Check one grade per enrollment
    existing_grade = db.query(Grade).filter(Grade.enrollment_id == grade.enrollment_id).first()
    if existing_grade:
        raise HTTPException(status_code=400, detail="Enrollment already has a grade")

    letter = compute_letter_grade(grade.score)
    new_grade = Grade(
        enrollment_id=grade.enrollment_id,
        score=grade.score,
        letter_grade=letter
    )
    db.add(new_grade)
    db.commit()
    db.refresh(new_grade)
    return new_grade

@router.get("/grades/{grade_id}", response_model=GradeResponse)
def get_grade(
    grade_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    grade = db.query(Grade).filter(Grade.id == grade_id).first()
    if not grade:
        raise HTTPException(status_code=404, detail="Grade not found")
    # Access control
    enrollment = grade.enrollment
    if current_user.role == "student" and enrollment.student_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    if current_user.role == "teacher" and enrollment.course.teacher_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    return grade

@router.put("/grades/{grade_id}", response_model=GradeResponse)
def update_grade(
    grade_id: int,
    grade_update: GradeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can update grades")
    grade = db.query(Grade).filter(Grade.id == grade_id).first()
    if not grade:
        raise HTTPException(status_code=404, detail="Grade not found")
    enrollment = grade.enrollment
    if enrollment.course.teacher_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only modify grades for your courses")
    if grade_update.score is not None:
        grade.score = grade_update.score
        grade.letter_grade = compute_letter_grade(grade_update.score)
    db.commit()
    db.refresh(grade)
    return grade

@router.delete("/grades/{grade_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_grade(
    grade_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can delete grades")
    grade = db.query(Grade).filter(Grade.id == grade_id).first()
    if not grade:
        raise HTTPException(status_code=404, detail="Grade not found")
    if grade.enrollment.course.teacher_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    db.delete(grade)
    db.commit()
    return

# ------------------- Assignments -------------------
@router.get("/assignments", response_model=List[AssignmentResponse])
def list_assignments(
    course_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Assignment)
    if course_id:
        query = query.filter(Assignment.course_id == course_id)
    assignments = query.all()
    # Filter access: students can only see assignments for courses they are enrolled in
    if current_user.role == "student":
        enrolled_course_ids = [e.course_id for e in current_user.enrollments]
        assignments = [a for a in assignments if a.course_id in enrolled_course_ids]
    # teachers can see assignments for their courses
    elif current_user.role == "teacher":
        allowed_courses = [c.id for c in current_user.taught_courses]
        assignments = [a for a in assignments if a.course_id in allowed_courses]
    return assignments

@router.post("/assignments", response_model=AssignmentResponse, status_code=status.HTTP_201_CREATED)
def create_assignment(
    assignment: AssignmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can create assignments")
    course = db.query(Course).filter(Course.id == assignment.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    if course.teacher_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only add assignments to your own courses")
    new_assignment = Assignment(**assignment.dict())
    db.add(new_assignment)
    db.commit()
    db.refresh(new_assignment)
    return new_assignment

@router.get("/assignments/{assignment_id}", response_model=AssignmentResponse)
def get_assignment(
    assignment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    # access control
    if current_user.role == "student":
        if assignment.course_id not in [e.course_id for e in current_user.enrollments]:
            raise HTTPException(status_code=403, detail="Not enrolled in this course")
    elif current_user.role == "teacher":
        if assignment.course.teacher_id != current_user.id:
            raise HTTPException(status_code=403, detail="Access denied")
    return assignment

@router.put("/assignments/{assignment_id}", response_model=AssignmentResponse)
def update_assignment(
    assignment_id: int,
    assignment_update: AssignmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can update assignments")
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    if assignment.course.teacher_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    update_data = assignment_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(assignment, key, value)
    db.commit()
    db.refresh(assignment)
    return assignment

@router.delete("/assignments/{assignment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_assignment(
    assignment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can delete assignments")
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    if assignment.course.teacher_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    db.delete(assignment)
    db.commit()
    return