from flask import render_template , redirect , flash , url_for
from . import student_bp
from flask_login import login_required , current_user

@student_bp.route("/dashboard" , methods=["GET" , "POST"])
@login_required
def student_dashboard():
    if current_user.role != "Stu":
        flash("Unauthorised User")
        return redirect(url_for("auth.login"))
    return render_template("student_dashboard.html" , student = current_user)