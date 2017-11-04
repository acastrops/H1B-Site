from flask import render_template, request, flash, redirect
from h1b import app
from sqlalchemy import func
from .forms import SearchForm
from .models import Cases, Employer

import sys


# Create index view, just as a default
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about-us/')
def about():
    return render_template('about.html')


@app.route('/results/<int:wage>')
def results(wage):
    # cases = Cases.query.filter(Cases.wage_rate > wage).order_by(Cases.wage_rate).limit(10)
    cases = Cases.query.filter(Cases.wage_rate.ilike('y%')).order_by(Cases.wage_rate).limit(10)
    ids = [case.employer_id for case in cases]
    print(ids, file=sys.stderr)
    employers = Employer.query.filter(Employer.id_.in_(ids)).all()

    data = zip(cases, employers)

    return render_template('results.html', data=data)


@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()

    if form.validate_on_submit():
        return redirect('/results/{}'.format(form.wage.data))

    return render_template('search.html', title='Search', form=form)


@app.route('/employer/<int:number>')
def employer(number):
    employer = Employer.query.filter_by(id_=number).first_or_404()
    return render_template('employer.html', employer=employer)
