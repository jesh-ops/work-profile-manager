from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app import db
from app.forms.company import CompanyForm
from app.models.company import Company

companies_bp = Blueprint("companies", __name__, url_prefix="/companies")


@companies_bp.route("/")
@login_required
def index():
    companies = Company.query.filter_by(user_id=current_user.id).order_by(Company.name.asc()).all()
    return render_template("companies/list.html", companies=companies)


@companies_bp.route("/new", methods=["GET", "POST"])
@login_required
def create():
    form = CompanyForm()
    if form.validate_on_submit():
        company = Company(
            user_id=current_user.id,
            name=form.name.data,
            description=form.description.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
        )
        db.session.add(company)
        db.session.commit()
        flash("Company created successfully.", "success")
        return redirect(url_for("companies.index"))
    return render_template("companies/create.html", form=form)


@companies_bp.route("/<int:company_id>")
@login_required
def detail(company_id):
    company = Company.query.filter_by(id=company_id, user_id=current_user.id).first_or_404()
    return render_template("companies/detail.html", company=company)


@companies_bp.route("/<int:company_id>/edit", methods=["GET", "POST"])
@login_required
def edit(company_id):
    company = Company.query.filter_by(id=company_id, user_id=current_user.id).first_or_404()
    form = CompanyForm(obj=company)
    if form.validate_on_submit():
        company.name = form.name.data
        company.description = form.description.data
        company.start_date = form.start_date.data
        company.end_date = form.end_date.data
        db.session.commit()
        flash("Company updated successfully.", "success")
        return redirect(url_for("companies.detail", company_id=company.id))
    return render_template("companies/edit.html", form=form, company=company)


@companies_bp.route("/<int:company_id>/delete", methods=["POST"])
@login_required
def delete(company_id):
    company = Company.query.filter_by(id=company_id, user_id=current_user.id).first_or_404()
    db.session.delete(company)
    db.session.commit()
    flash("Company deleted.", "success")
    return redirect(url_for("companies.index"))
