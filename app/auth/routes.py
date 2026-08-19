from app.auth import auth_bp
from flask import flash , render_template , redirect , url_for
from app.auth.forms import Registeration_form , Login_form
from app.models import User
from app.extensions import db , bcrypt
from flask_login import login_user , login_required , logout_user
@auth_bp.route("/register" , methods=["GET","POST"])
def register():
    form = Registeration_form()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email = form.email.data).first()
        if existing_user:
            flash("User Already Exist...." , "danger")
            return redirect(url_for("auth.register"))
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(
        name = form.name.data, 
        email = form.email.data, 
        password = hashed_password, 
        phone_number = form.phone_number.data, 
        role = form.role.data
        ) 
        db.session.add(user)
        db.session.commit()
        flash ("Registeration Sucessfull" , "success")
        return redirect(url_for("auth.login"))
    return render_template("auth.register.html" , form=form)

@auth_bp.route("/login" , methods=["GET" , "POST"])
def login():
    form = Login_form()
    if form.validate_on_submit():
        existing_user = User.query.filter_by( email= form.email.data).first()
        if existing_user:
            if bcrypt.check_password_hash(existing_user.password , form.password.data):
                login_user(existing_user)
                flash("Login Sucessfully" , "success")
                if existing_user.role == "Stu":
                    return redirect(url_for("student.student_dashboard"))
                else:
                    return redirect(url_for("Instructor.instructor_dashboard"))
            flash("Invalid Email/Password" , "danger")
            return render_template("auth.login.html" , form=form)
        flash("Invalid Email/Password" , "danger")
        return render_template("auth.login.html" , form=form)
    return render_template("auth.login.html" , form = form)

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logout Successfully" , "success")
    return redirect(url_for("auth.login"))