from flask import Flask
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View

nav = Nav()

nav.register_element('top', Navbar(
    View('Main', '.index'),
    View('About', '.about')
))

app = Flask(__name__)
Bootstrap(app)
nav.init_app(app)

import h1b.views
