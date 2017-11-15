from flask import render_template, request, flash, redirect
from h1b import app
from sqlalchemy import func, and_, desc, extract
from .forms import SearchForm
from . import db
from .models import Cases, Employer
from .helpers import create_cases_by_state, create_wages_by_state, create_wages_by_year

import sys


# Create index view, just as a default
@app.route('/')
def index():
    script_case, div_case, js_case, css_case = create_cases_by_state()
    script_wage, div_wage, js_wage, css_wage = create_wages_by_state()
    script_wby, div_wby, js_wby, css_wby = create_wages_by_year()

    return render_template('index.html', div_case=div_case, script_case=script_case, js_case=js_case, css_case=css_case,
                           div_wage=div_wage, script_wage=script_wage, js_wage=js_wage, css_wage=css_wage, script_wby=script_wby, div_wby=div_wby, js_wby=js_wby, css_wby=css_wby)


@app.route('/about-us/')
def about():
    return render_template('about.html')


# oh god don't look at this part
@app.route('/results/<int:wage_low>/<int:wage_high>/<state>')
def results(wage_low, wage_high, state):
    res = db.session.query(Cases, Employer).filter(and_(Cases.real_wage > wage_low,
                                  Cases.real_wage < wage_high))
    res = res.join(Employer, Cases.employer_id==Employer.id_).filter(Employer.state.match(state))
    res = res.order_by(desc(Cases.begin_date)).all()
    
    return render_template('results.html', data=res)


@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()

    # if form.validate_on_submit():
    if request.method == 'POST':
        return redirect('/results/{}/{}/{}'.format(form.wage_low.data, form.wage_high.data, form.state.data))

    return render_template('search.html', title='Search', form=form)


@app.route('/employer/<int:number>')
def employer(number):
    employer = Employer.query.filter_by(id_=number).first_or_404()
    return render_template('employer.html', employer=employer)
