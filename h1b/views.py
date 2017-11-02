from flask import render_template, request, flash, redirect
from h1b import app
from .forms import EmployerSearchForm
from .models import Cases, Employer

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
