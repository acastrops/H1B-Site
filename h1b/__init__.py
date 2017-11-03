from flask import Flask
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View
from flask_sqlalchemy import SQLAlchemy

nav = Nav()

nav.register_element('top', Navbar(
    View('Main', '.index'),
    View('Search', '.search'),
    View('About', '.about'),
))

app = Flask(__name__)
app.config.from_envvar('H1B_SETTINGS')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
Bootstrap(app)
nav.init_app(app)

db = SQLAlchemy()
db.init_app(app)

import h1b.views
