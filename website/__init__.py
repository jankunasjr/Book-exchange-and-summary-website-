from flask import Flask
from website.extensions import db  # Import db from your extensions module
from config import SQLALCHEMY_DATABASE_URI, \
    SQLALCHEMY_TRACK_MODIFICATIONS, ollama_llm
from flask_login import LoginManager
from website.models import UserRoleEnum


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'pkpjauperdaug'
    # Load the SQLAlchemy configuration from config.py
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    #app.config['SQLALCHEMY_TEST_DATABASE_URI'] = SQLALCHEMY_TEST_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
    app.config['OLLAMA_LLM'] = ollama_llm

    db.init_app(app)  # Initialize db with the app

    with app.app_context():
        # Import models to ensure they are registered with SQLAlchemy
        from . import models

    from .views import views
    from .auth import auth
    from .models import Users
    from .inventory import inventory
    from .trades import trades
    from .prompts import prompts_bp
    from .profile import profile
    from .admin import admin

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(inventory, url_prefix='/')
    app.register_blueprint(trades, url_prefix='/')
    app.register_blueprint(prompts_bp, url_prefix='/prompt')
    app.register_blueprint(profile, url_prefix='/profile')
    app.register_blueprint(admin, url_prefix='/admin')

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @app.context_processor
    def inject_enums():
        return dict(UserRoleEnum=UserRoleEnum)

    @login_manager.user_loader
    def load_user(UserID):
        return Users.query.get(int(UserID))

    return app
