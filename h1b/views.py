from flask import render_template
from h1b import app


# Create index view, just as a default
@app.route('/')
def show_index():
    return render_template('index.html')
