from app.extensions import db , login_manager , bcrypt, migrate
from flask import Flask
from config import Config
from .auth import auth_bp
from .student import student_bp
from .instructor import instructor_bp
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    from app.models import User
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    @login_manager.user_loader
    def load_user(user_id):
       return User.query.get(int(user_id))
    bcrypt.init_app(app)
    migrate.init_app(app , db)
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(instructor_bp)
    return app 
