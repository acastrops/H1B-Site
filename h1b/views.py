from flask import render_template, request, flash, redirect
from h1b import app
from .forms import EmployerSearchForm
from .models import Cases, Employer
from .helpers import create_cases_by_state, create_wages_by_state

import sys


# Create index view, just as a default
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about-us/')
def about():
    return render_template('about.html')


@app.route('/case/<int:number>')
def case(number):
    case = Cases.query.filter_by(id_=number).first_or_404()
    return render_template('case.html', case=case)


@app.route('/search', methods=['GET', 'POST'])
def search():
    form = EmployerSearchForm()

    if form.validate_on_submit():
        return redirect('/employer/{}'.format(form.id_.data))

    return render_template('search.html', title='Search', form=form)


@app.route('/employer/<int:number>')
def employer(number):
    employer = Employer.query.filter_by(id_=number).first_or_404()
    return render_template('employer.html', employer=employer)


@app.route('/graph_test')
def graph_test():
    script_case, div_case, js_case, css_case = create_cases_by_state()
    script_wage, div_wage, js_wage, css_wage = create_wages_by_state()

    return render_template('graph_test.html', div_case=div_case, script_case=script_case, js_case=js_case, css_case=css_case,
                           div_wage=div_wage, script_wage=script_wage, js_wage=js_wage, css_wage=css_wage)
