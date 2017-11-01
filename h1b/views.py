from .models import Cases, JobCode

from flask import render_template
from h1b import app
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


@app.route('/job/<code>')
def job_code(code):
    job = JobCode.query.filter_by(code=code).first_or_404()
    return render_template('job_code.html', job=job)
