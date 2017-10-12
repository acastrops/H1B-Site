import os
from subprocess import call

call(['pip', 'install', '--editable', '.'])

os.environ['FLASK_APP'] = 'h1b'

# Change to false in production
os.environ['FLASK_DEBUG'] = 'true'

call(['flask', 'run'])
