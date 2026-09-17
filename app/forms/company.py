from flask_wtf import FlaskForm
from wtforms import DateField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Optional


class CompanyForm(FlaskForm):
    name = StringField("Company name", validators=[DataRequired()])
    description = TextAreaField("Description")
    start_date = DateField("Start date", format="%Y-%m-%d", validators=[Optional()])
    end_date = DateField("End date", format="%Y-%m-%d", validators=[Optional()])
    submit = SubmitField("Save company")
