from flask import Flask
from website.extensions import db  # Import db from your extensions module
from config import SQLALCHEMY_DATABASE_URI, \
    SQLALCHEMY_TRACK_MODIFICATIONS  # Assuming these are defined in your config.py
from flask_login import LoginManager

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'pkpjauperdaug'
    # Load the SQLAlchemy configuration from config.py
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
    app.config['OLLAMA_LLM'] = "/Users/paulius/.ollama/models/blobs/sha256-8934d96d3f08982e95922b2b7a2c626a1fe873d7c3b06e8e56d7bc0a1fef9246"

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

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(inventory, url_prefix='/')
    app.register_blueprint(trades, url_prefix='/')
    app.register_blueprint(prompts_bp, url_prefix='/prompt')

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(UserID):
        return Users.query.get(int(UserID))

    return app
