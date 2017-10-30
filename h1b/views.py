from flask import render_template
from h1b import app


# Create index view, just as a default
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about-us/')
def about():
    return render_template('about.html')
