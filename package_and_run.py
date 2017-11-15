import os
from subprocess import call

call(['pip3', 'install', '--editable', '.'])

os.environ['FLASK_APP'] = 'h1b'
os.environ['H1B_SETTINGS'] = './instance/config.py'

call(['python3', '-m', 'flask', 'run'])
