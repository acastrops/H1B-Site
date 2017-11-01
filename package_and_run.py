import os
from subprocess import call

call(['pip', 'install', '--editable', '.'])

os.environ['FLASK_APP'] = 'h1b'
os.environ['H1B_SETTINGS'] = './instance/config.py'

call(['flask', 'run'])
