from flask import render_template , redirect , flash , url_for
from . import student_bp
from flask_login import login_required , current_user
from app.models import Enrollement , Course , CourseStatus , Lesson
from .forms import EnrollementForm
from app.extensions import db
@student_bp.route("/dashboard" , methods=["GET" , "POST"])
@login_required
def student_dashboard():
    if current_user.role != "Stu":
        flash("Unauthorised User")
        return redirect(url_for("auth.login"))
    
    enrollement = Enrollement.query.filter_by(student_id = current_user.id).all()
    
    enrolled_courses_ids = [enroll.course_id for enroll in enrollement]
    
    avail_course = Course.query.filter(
        Course.status == CourseStatus.PUBLISH ,
        ~Course.id.in_(enrolled_courses_ids)
        ).all()
    
    return render_template(
        "student_dashboard.html" ,
        student = current_user ,
        enrollement=enrollement,
        avail_course = avail_course
        )

@student_bp.route("/course_detail/<int:course_id>")
@login_required
def course_detail(course_id):
    
    if current_user.role != "Stu":
        flash("Unauthorized User","danger")
        return redirect(url_for("auth.login"))
    
    course = Course.query.get_or_404(course_id)
    
    return render_template("Student_course_detail.html" , course=course)

@student_bp.route("/enroll_course/<int:course_id>" , methods=["GET" , "POST"])
@login_required
def enroll_course(course_id):
    if current_user.role != "Stu":
        flash("Unauthorized User","danger")
        return redirect(url_for("auth.login"))
    
    existing_course = Course.query.get_or_404(course_id)

    if existing_course.status.value != "publish":
        flash("Course is not available for enrollement" , "danger")
        return redirect(url_for("student.student_dashboard"))
    
    existing_enrollement = Enrollement.query.filter_by(
        student_id = current_user.id,
        course_id = existing_course.id
    ).first()
    
    if existing_enrollement:
        flash("You Have Already Enrolled in This Course")
        return redirect(url_for("student.student_dashboard"))
    
    form = EnrollementForm()
    
    if form.validate_on_submit():
        enroll = Enrollement(
            student_id = current_user.id,
            course_id = existing_course.id
        )
        
        db.session.add(enroll)
        db.session.commit()
        
        flash("Successfully enrolled" , "success")
        return redirect(url_for("student.student_dashboard"))
    
    return render_template(
        "enroll_course.html",
        course = existing_course,
        form = form
        )
    

@student_bp.route("/course/<int:course_id>/lesson/<int:lesson_id>")
@login_required
def lesson_detail(course_id , lesson_id):
    
    if current_user.role != "Stu":
        flash("Unauthorised User" , "danger")
        return redirect(url_for("auth.login"))
    
    course = Course.query.get_or_404(course_id)
    
    enrolled = Enrollement.query.filter_by(
                    student_id = current_user.id,
                    course_id = course.id
                    ).first()
    
    if not enrolled :
        flash("You Are Not Enrolled To This Course" , "danger")
        return redirect(url_for("student.student_dashboard"))
    
    lesson = Lesson.query.get_or_404(lesson_id)
    
    if lesson.course_id != course.id:
        flash("Invalid Course","danger")
        return redirect(url_for("student.course_detail",
                                course_id = course.id))
        
    return render_template(
        "student_lesson_detail.html",
        course = course,
        lesson = lesson
    )
    

    
    