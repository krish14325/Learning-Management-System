from flask import Blueprint
instructor_bp = Blueprint("Instructor" , __name__ , url_prefix="/instructor")
from . import routes