from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from config import Config


db = SQLAlchemy()
csrf = CSRFProtect()
login_manager = LoginManager()
login_manager.login_view = "main.login"
login_manager.login_message = "Будь ласка, увійдіть, щоб продовжити."


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)

    app.config["STL_UPLOAD_FOLDER"].mkdir(parents=True, exist_ok=True)
    app.config["PHOTO_UPLOAD_FOLDER"].mkdir(parents=True, exist_ok=True)

    from .routes import main_bp

    app.register_blueprint(main_bp)

    with app.app_context():
        db.create_all()

    return app
