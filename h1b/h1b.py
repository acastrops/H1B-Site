import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

import psycopg2

## Initialize the 'h1b' app and load in the sooper secret keys
app = Flask(__name__)
app.config.from_object(__name__)


with open('./h1b/secrets') as f:
	lines = f.read().splitlines()
keys = dict([line.split('::::') for line in lines if line[0] != '#'])

app.config.update(dict(
	DATABASE = keys['H1BDB_HOST'],
	SECRET_KEY = keys['SECRET_KEY'],
	USERNAME = keys['H1BDB_USERNAME'],
	PASSWORD = keys['H1BDB_PASSWORD']
))

app.config.from_envvar('FLASKR_SETTINGS', silent=True)

## Create index view, just as a default
@app.route('/')
def show_index():
	return render_template('index.html')

## Initialize the database connection settings
## TODO: Split into new file, but not neccessary until the database is populated
#from sqlalchemy import create_engine
#from sqlalchemy import Column, String
#from sqlalchemy.ext.declarative import declarative_base  
#from sqlalchemy.orm import sessionmaker
#db_string = 'postgresql+psycopg2://{1}:{2}@{3}:5432/h1bdb'.format(keys['H1BDB_PASSWORD'], keys['H1BDB_USERNAME'], keys['H1BDB_HOST'])
#db = create_engine(db_string)
