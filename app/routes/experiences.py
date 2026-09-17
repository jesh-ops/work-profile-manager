from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app import db
from app.forms.experience import ExperienceForm
from app.models.company import Company
from app.models.experience import Experience
from app.models.project import Project
from app.models.role import Role
from app.models.tag import Tag

experiences_bp = Blueprint("experiences", __name__, url_prefix="/experiences")


def get_company_options():
    return [(company.id, company.name) for company in Company.query.filter_by(user_id=current_user.id).order_by(Company.name.asc()).all()]


def get_project_options(company_id=None):
    query = Project.query.filter_by(user_id=current_user.id)
    if company_id:
        query = query.filter_by(company_id=company_id)
    return [(project.id, project.name) for project in query.order_by(Project.name.asc()).all()]


def get_role_options(company_id=None):
    query = Role.query.filter_by(user_id=current_user.id)
    if company_id:
        query = query.filter_by(company_id=company_id)
    return [(role.id, role.title) for role in query.order_by(Role.title.asc()).all()]


@experiences_bp.route("/")
@login_required
def index():
    experiences = Experience.query.filter_by(user_id=current_user.id).order_by(Experience.experience_date.desc(), Experience.created_at.desc()).all()
    return render_template("experiences/list.html", experiences=experiences)


@experiences_bp.route("/new", methods=["GET", "POST"])
@login_required
def create():
    form = ExperienceForm()
    form.company_id.choices = get_company_options()
    form.project_id.choices = get_project_options(form.company_id.data or None)
    form.role_id.choices = [(-1, "No role selected")] + get_role_options(form.company_id.data or None)

    if form.validate_on_submit():
        if form.role_id.data == -1:
            role_id = None
        else:
            role_id = form.role_id.data

        experience = Experience(
            user_id=current_user.id,
            company_id=form.company_id.data,
            project_id=form.project_id.data,
            role_id=role_id,
            title=form.title.data,
            experience_date=form.experience_date.data,
            context=form.context.data,
            problem=form.problem.data,
            investigation=form.investigation.data,
            action=form.action.data,
            result=form.result.data,
            lessons_learned=form.lessons_learned.data,
        )

        tag_names = [tag.strip() for tag in form.tags.data.split(",") if tag.strip()]
        for tag_name in tag_names:
            tag = Tag.query.filter_by(user_id=current_user.id, name=tag_name).first()
            if not tag:
                tag = Tag(user_id=current_user.id, name=tag_name)
                db.session.add(tag)
            experience.tags.append(tag)

        db.session.add(experience)
        db.session.commit()
        flash("Experience created successfully.", "success")
        return redirect(url_for("experiences.index"))

    return render_template("experiences/create.html", form=form)


@experiences_bp.route("/<int:experience_id>")
@login_required
def detail(experience_id):
    experience = Experience.query.filter_by(id=experience_id, user_id=current_user.id).first_or_404()
    return render_template("experiences/detail.html", experience=experience)


@experiences_bp.route("/<int:experience_id>/edit", methods=["GET", "POST"])
@login_required
def edit(experience_id):
    experience = Experience.query.filter_by(id=experience_id, user_id=current_user.id).first_or_404()
    form = ExperienceForm(obj=experience)
    form.company_id.choices = get_company_options()
    form.project_id.choices = get_project_options(experience.company_id)
    form.role_id.choices = [(-1, "No role selected")] + get_role_options(experience.company_id)
    form.tags.data = ", ".join(tag.name for tag in experience.tags)

    if form.validate_on_submit():
        experience.company_id = form.company_id.data
        experience.project_id = form.project_id.data
        experience.role_id = None if form.role_id.data == -1 else form.role_id.data
        experience.title = form.title.data
        experience.experience_date = form.experience_date.data
        experience.context = form.context.data
        experience.problem = form.problem.data
        experience.investigation = form.investigation.data
        experience.action = form.action.data
        experience.result = form.result.data
        experience.lessons_learned = form.lessons_learned.data

        experience.tags.clear()
        for tag_name in [tag.strip() for tag in form.tags.data.split(",") if tag.strip()]:
            tag = Tag.query.filter_by(user_id=current_user.id, name=tag_name).first()
            if not tag:
                tag = Tag(user_id=current_user.id, name=tag_name)
                db.session.add(tag)
            experience.tags.append(tag)

        db.session.commit()
        flash("Experience updated successfully.", "success")
        return redirect(url_for("experiences.detail", experience_id=experience.id))

    return render_template("experiences/edit.html", form=form, experience=experience)


@experiences_bp.route("/<int:experience_id>/delete", methods=["POST"])
@login_required
def delete(experience_id):
    experience = Experience.query.filter_by(id=experience_id, user_id=current_user.id).first_or_404()
    db.session.delete(experience)
    db.session.commit()
    flash("Experience deleted.", "success")
    return redirect(url_for("experiences.index"))
