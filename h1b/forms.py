from flask_wtf import Form
from wtforms import IntegerField
from wtforms.validators import DataRequired


class EmployerSearchForm(Form):
    id_ = IntegerField('number', validators=[DataRequired()])
