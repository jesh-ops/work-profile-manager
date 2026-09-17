from flask import Blueprint, render_template
from flask_login import current_user, login_required

from app.models.company import Company
from app.models.experience import Experience
from app.models.project import Project
from app.models.role import Role


dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/")


@dashboard_bp.route("/dashboard")
@login_required
def index():
    companies_count = Company.query.filter_by(user_id=current_user.id).count()
    projects_count = Project.query.filter_by(user_id=current_user.id).count()
    roles_count = Role.query.filter_by(user_id=current_user.id).count()
    experiences_count = Experience.query.filter_by(user_id=current_user.id).count()

    return render_template(
        "dashboard/index.html",
        companies_count=companies_count,
        projects_count=projects_count,
        roles_count=roles_count,
        experiences_count=experiences_count,
    )
