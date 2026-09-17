from flask import Flask, redirect, render_template, url_for
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

from config import config

load_dotenv()


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message_category = "info"


@login_manager.user_loader
def load_user(user_id):
    from app.models.user import User

    return User.query.get(int(user_id))


def create_app(config_name: str = "default"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from app.models.company import Company
    from app.models.experience import Experience
    from app.models.project import Project
    from app.models.role import Role
    from app.models.tag import Tag
    from app.models.user import User

    @app.route("/")
    def index():
        from flask_login import current_user

        if current_user.is_authenticated:
            return redirect(url_for("dashboard.index"))
        return redirect(url_for("auth.login"))

    from app.routes.auth import auth_bp
    from app.routes.companies import companies_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.experiences import experiences_bp
    from app.routes.projects import projects_bp
    from app.routes.roles import roles_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(companies_bp)
    app.register_blueprint(projects_bp)
    app.register_blueprint(roles_bp)
    app.register_blueprint(experiences_bp)

    from pathlib import Path

    upload_dir = Path(app.config["UPLOAD_FOLDER"])
    upload_dir.mkdir(parents=True, exist_ok=True)

    with app.app_context():
        db.create_all()

    return app
