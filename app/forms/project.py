from flask_wtf import FlaskForm
from wtforms import DateField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Optional


class ProjectForm(FlaskForm):
    company_id = SelectField("Company", coerce=int, validators=[DataRequired()])
    name = StringField("Project name", validators=[DataRequired()])
    description = TextAreaField("Description")
    start_date = DateField("Start date", format="%Y-%m-%d", validators=[Optional()])
    end_date = DateField("End date", format="%Y-%m-%d", validators=[Optional()])
    status = SelectField(
        "Status",
        choices=[
            ("planned", "Planned"),
            ("active", "Active"),
            ("completed", "Completed"),
            ("on_hold", "On hold"),
        ],
        default="active",
    )
    submit = SubmitField("Save project")
