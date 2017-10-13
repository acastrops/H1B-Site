import os
from subprocess import call

call(['pip', 'install', '--editable', '.'])

os.environ['FLASK_APP'] = 'h1b'

call(['flask', 'run'])
