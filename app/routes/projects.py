from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app import db
from app.forms.project import ProjectForm
from app.models.company import Company
from app.models.project import Project

projects_bp = Blueprint("projects", __name__, url_prefix="/projects")


@projects_bp.route("/")
@login_required
def index():
    projects = Project.query.filter_by(user_id=current_user.id).order_by(Project.start_date.desc().nullslast(), Project.name.asc()).all()
    return render_template("projects/list.html", projects=projects)


@projects_bp.route("/new", methods=["GET", "POST"])
@login_required
def create():
    form = ProjectForm()
    form.company_id.choices = [(company.id, company.name) for company in Company.query.filter_by(user_id=current_user.id).order_by(Company.name.asc()).all()]

    if form.validate_on_submit():
        project = Project(
            user_id=current_user.id,
            company_id=form.company_id.data,
            name=form.name.data,
            description=form.description.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            status=form.status.data,
        )
        db.session.add(project)
        db.session.commit()
        flash("Project created successfully.", "success")
        return redirect(url_for("projects.index"))
    return render_template("projects/create.html", form=form)


@projects_bp.route("/<int:project_id>")
@login_required
def detail(project_id):
    project = Project.query.filter_by(id=project_id, user_id=current_user.id).first_or_404()
    return render_template("projects/detail.html", project=project)


@projects_bp.route("/<int:project_id>/edit", methods=["GET", "POST"])
@login_required
def edit(project_id):
    project = Project.query.filter_by(id=project_id, user_id=current_user.id).first_or_404()
    form = ProjectForm(obj=project)
    form.company_id.choices = [(company.id, company.name) for company in Company.query.filter_by(user_id=current_user.id).order_by(Company.name.asc()).all()]

    if form.validate_on_submit():
        project.company_id = form.company_id.data
        project.name = form.name.data
        project.description = form.description.data
        project.start_date = form.start_date.data
        project.end_date = form.end_date.data
        project.status = form.status.data
        db.session.commit()
        flash("Project updated successfully.", "success")
        return redirect(url_for("projects.detail", project_id=project.id))
    return render_template("projects/edit.html", form=form, project=project)


@projects_bp.route("/<int:project_id>/delete", methods=["POST"])
@login_required
def delete(project_id):
    project = Project.query.filter_by(id=project_id, user_id=current_user.id).first_or_404()
    db.session.delete(project)
    db.session.commit()
    flash("Project deleted.", "success")
    return redirect(url_for("projects.index"))
