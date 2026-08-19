from flask import flash , redirect , render_template , url_for
from . import instructor_bp
from flask_login import current_user , login_required
from app.models import Course , Lesson
from .forms import Course_create , lesson_create , Deletelessonform
from app.extensions import db
@instructor_bp.route("/dashboard" , methods=["GET" , "POST"])
@login_required
def instructor_dashboard():
    if current_user.role != "Tea":
        flash("Unauthorised User")
        return redirect(url_for("auth.login"))
    
    course = Course.query.filter_by(teacher_id = current_user.id).all()
    return render_template("instructor.dashboard.html" , instructor=current_user ,  courses=course)

@instructor_bp.route("/Create_Course" , methods=["GET" , "POST"])
@login_required
def createcourse():
    form = Course_create()
    if form.validate_on_submit():
        existing_course = Course.query.filter_by(title = form.title.data).first()
        existing_user_courses  = Course.query.filter_by(teacher_id = current_user.id).all()
        if existing_course not in existing_user_courses:
            course = Course(
                title = form.title.data,
                description = form.description.data,
                teacher_id = current_user.id
            )
            db.session.add(course)
            db.session.commit()
            flash("Course Created Sucessfully!" , "success")
            return redirect(url_for("Instructor.createcourse"))
        flash("Course Already Existed" , "danger")
        return redirect(url_for("Instructor.instructor_dashboard"))
    return render_template("createcourse.html" , form=form)

@instructor_bp.route("/course/<int:course_id>")
@login_required
def course_detail(course_id):

    course = Course.query.filter_by(
        id=course_id ,
        teacher_id = current_user.id
        ).first()
    
    if not course:
        flash("Course Not Found or Unauthorised User" , "danger")
        return redirect(url_for("Instructor.instructor_dashboard"))
    
    return render_template(
        "coursedetail.html" ,
        instructor=current_user ,
        course=course
        )
    
@instructor_bp.route("/course/<int:course_id>/add_lesson" , methods=["GET" , "POST"])
@login_required
def add_lesson(course_id):
    course = Course.query.filter_by(
        id = course_id ,
        teacher_id = current_user.id
        ).first()
    if not course:
        flash("No Course Found or Unauthorised User" , "danger")
        return redirect(url_for("Instructor.instructor_dashboard"))
    form = lesson_create()
    if form.validate_on_submit():
        lesson = Lesson(
            title = form.title.data,
            content = form.content.data,
            position = form.position.data,
            course_id = course_id
        )
        db.session.add(lesson)
        db.session.commit()
        flash("Lesson Added Successfully" , "success")
        return redirect(url_for("Instructor.course_detail" , course_id = course.id))
    return render_template("add_lesson.html" , form=form , course=course)

@instructor_bp.route("course/<int:course_id>/lesson/<int:lesson_id>")
@login_required
def lesson_info(course_id  , lesson_id):
    
    course = Course.query.filter_by(id = course_id , 
                                    teacher_id = current_user.id
                                    ).first()
    
    lesson = Lesson.query.filter_by(id = lesson_id ,
                                    course_id = course.id
                                    ).first()
    
    form = Deletelessonform()
    return render_template(
                        "lesson_detail.html" ,
                        course = course ,
                        lesson = lesson,
                        form = form
                        )
    
@instructor_bp.route("/course/<int:course_id>/lesson/<int:lesson_id>/lesson_edit" , methods=["GET" , "POST"])
@login_required
def lesson_edit(course_id , lesson_id):
    course = Course.query.filter_by(id = course_id ,
                                    teacher_id = current_user.id
                                    ).first()
    lesson = Lesson.query.filter_by(id = lesson_id,
                                    course_id = course.id
                                    ).first()
    
    form = lesson_create(obj = lesson)
    
    if form.validate_on_submit():
        lesson.title = form.title.data,
        lesson.content = form.content.data,
        lesson.position = form.position.data
        
        db.session.commit()
        
        flash("Changes Added Successfully" , "success")
        return redirect(
            url_for(
                "Instructor.lesson_info" ,
                course_id = course.id ,
                lesson_id = lesson.id)
                        )
    
    return render_template("lesson_edit.html" , form=form , lesson=lesson , course = course)

@instructor_bp.route("/course/<int:course_id>/lesson/<int:lesson_id>/delete",methods=["POST"])
@login_required
def delete_lesson(course_id , lesson_id):
    course = Course.query.filter_by( id = course_id , teacher_id =  current_user.id).first()
    lesson = Lesson.query.filter_by( id = lesson_id , course_id =  course.id).first()
    
    db.session.delete(lesson)
    db.session.commit()
    
    flash("Lesson Deleted Successfully" , "success")
    return redirect(url_for("Instructor.course_detail" , course_id = course.id))
    