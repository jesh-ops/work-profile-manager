from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app import db
from app.models.company import Company
from app.models.role import Role

roles_bp = Blueprint("roles", __name__, url_prefix="/roles")


@roles_bp.route("/")
@login_required
def index():
    roles = Role.query.filter_by(user_id=current_user.id).order_by(Role.start_date.desc().nullslast(), Role.title.asc()).all()
    return render_template("roles/list.html", roles=roles)


@roles_bp.route("/new", methods=["GET", "POST"])
@login_required
def create():
    companies = Company.query.filter_by(user_id=current_user.id).order_by(Company.name.asc()).all()
    if request.method == "POST":
        company_id = request.form.get("company_id")
        title = request.form.get("title")
        description = request.form.get("description")
        start_date = request.form.get("start_date") or None
        end_date = request.form.get("end_date") or None

        if not company_id or not title:
            flash("Company and title are required.", "danger")
            return render_template("roles/create.html", companies=companies)

        role = Role(
            user_id=current_user.id,
            company_id=int(company_id),
            title=title,
            description=description,
            start_date=start_date,
            end_date=end_date,
        )
        db.session.add(role)
        db.session.commit()
        flash("Role created successfully.", "success")
        return redirect(url_for("roles.index"))

    return render_template("roles/create.html", companies=companies)


@roles_bp.route("/<int:role_id>")
@login_required
def detail(role_id):
    role = Role.query.filter_by(id=role_id, user_id=current_user.id).first_or_404()
    return render_template("roles/detail.html", role=role)


@roles_bp.route("/<int:role_id>/edit", methods=["GET", "POST"])
@login_required
def edit(role_id):
    role = Role.query.filter_by(id=role_id, user_id=current_user.id).first_or_404()
    companies = Company.query.filter_by(user_id=current_user.id).order_by(Company.name.asc()).all()

    if request.method == "POST":
        role.company_id = request.form.get("company_id")
        role.title = request.form.get("title")
        role.description = request.form.get("description")
        role.start_date = request.form.get("start_date") or None
        role.end_date = request.form.get("end_date") or None
        db.session.commit()
        flash("Role updated successfully.", "success")
        return redirect(url_for("roles.detail", role_id=role.id))

    return render_template("roles/edit.html", role=role, companies=companies)


@roles_bp.route("/<int:role_id>/delete", methods=["POST"])
@login_required
def delete(role_id):
    role = Role.query.filter_by(id=role_id, user_id=current_user.id).first_or_404()
    db.session.delete(role)
    db.session.commit()
    flash("Role deleted.", "success")
    return redirect(url_for("roles.index"))
