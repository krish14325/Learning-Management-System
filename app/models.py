from datetime import datetime
from flask_login import UserMixin
from app.extensions import db
from enum import Enum

class User(db.Model , UserMixin):
    __tablename__ = "users"
    id =  db.Column(db.Integer , primary_key = True )
    name =  db.Column(db.String(100) , nullable=False )
    email =  db.Column(db.String(100) , unique=True , nullable=False)
    password =  db.Column(db.String(255) , nullable = False )
    phone_number =  db.Column(db.String(15) , nullable=False )
    role = db.Column(db.String(20) , nullable = False )
    created_at = db.Column(db.DateTime ,  default= datetime.utcnow ) 
    courses = db.relationship("Course" , back_populates="teacher")
    enrollements = db.relationship("Enrollement" , back_populates="student")
    
class CourseStatus(Enum):
    DRAFT = "draft"
    PUBLISH = "publish"
    
class Course(db.Model):
    __tablename__ = "courses"
    id = db.Column(db.Integer , primary_key = True )
    title = db.Column(db.String(100) , nullable=False)
    description = db.Column(db.Text , nullable=False)
    
    teacher_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )
    
    status = db.Column(
        db.Enum(CourseStatus),
        nullable=False,
        default=CourseStatus.DRAFT
    )
    
    teacher = db.relationship("User" , back_populates="courses")
    
    lessons = db.relationship("Lesson" , back_populates="course")
    
    enrollements = db.relationship("Enrollement" , back_populates="course")
    
class Lesson(db.Model):
    __tablename__ = "lessons"
    id = db.Column(db.Integer , primary_key=True )
    title = db.Column(db.String(100) , nullable=False )
    content = db.Column(db.Text , nullable = False)
    position = db.Column(db.Integer , nullable=False )
    course_id = db.Column(db.Integer , db.ForeignKey("courses.id") , nullable=False )
    
    course = db.relationship("Course" , back_populates="lessons")
    lesson_progress = db.relationship("LessonProgress" , back_populates="lesson")
    
class Enrollement(db.Model):
    __tablename__ = "enrollements"
    id = db.Column(db.Integer , primary_key = True)
    student_id = db.Column(db.Integer , db.ForeignKey("users.id") , nullable=False)
    course_id = db.Column(db.Integer , db.ForeignKey("courses.id") , nullable = False )
    progress = db.Column(db.Integer ,default=0, nullable = False )
    enrolled_at = db.Column(db.DateTime , default=datetime.utcnow , nullable = False )
    __table_args__ = (
        db.UniqueConstraint(
            "student_id",
            "course_id" , 
            name = "unique_student_course"
        ),
    )
    student = db.relationship("User" , back_populates="enrollements")
    course = db.relationship("Course" , back_populates="enrollements")
    lesson_progress = db.relationship("LessonProgress" , back_populates="enrollement")
    
class LessonProgress(db.Model):
    __tablename__ = "lessonprogress"
    id = db.Column(db.Integer , primary_key = True )
    enrollment_id = db.Column(db.Integer , db.ForeignKey("enrollements.id") , nullable=False)
    lesson_id = db.Column(db.Integer , db.ForeignKey("lessons.id") , nullable = False )
    completed = db.Column(db.Boolean , nullable=False , default=False )
    __table_args__ = (
        db.UniqueConstraint(
            "enrollment_id",
            "lesson_id",
            name="unique_enrollment_lesson"
        ),
    )
    enrollement = db.relationship("Enrollement" , back_populates="lesson_progress")
    lesson = db.relationship("Lesson" , back_populates="lesson_progress")