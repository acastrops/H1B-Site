from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField
from wtforms.validators import Optional


states = ('AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 
          'HI', 'ID', 'IL', 'IN', 'IO', 'KS', 'KY', 'LA', 'ME', 'MD', 
          'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 
          'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 
          'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY')

class SearchForm(FlaskForm):
    wage_low = IntegerField('wage_low', [Optional()])
    wage_high = IntegerField('wage_high', [Optional()])
    state = SelectField('state', choices = zip(states, states))
