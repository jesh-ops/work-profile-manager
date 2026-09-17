from flask_wtf import FlaskForm
from wtforms import DateField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class ExperienceForm(FlaskForm):
    company_id = SelectField("Company", coerce=int, validators=[DataRequired()])
    project_id = SelectField("Project", coerce=int, validators=[DataRequired()])
    role_id = SelectField("Role", coerce=int, validators=[DataRequired()], default=None)
    title = StringField("Title", validators=[DataRequired()])
    experience_date = DateField("Date", format="%Y-%m-%d", validators=[DataRequired()])
    context = TextAreaField("Context", validators=[DataRequired()])
    problem = TextAreaField("Problem", validators=[DataRequired()])
    investigation = TextAreaField("Investigation", validators=[DataRequired()])
    action = TextAreaField("Action", validators=[DataRequired()])
    result = TextAreaField("Result", validators=[DataRequired()])
    lessons_learned = TextAreaField("Lessons learned", validators=[DataRequired()])
    tags = StringField("Tags")
    submit = SubmitField("Save experience")
