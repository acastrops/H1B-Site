from h1b import app
from .models import db

# Initialize the 'h1b' app and load in the sooper secret keys
app.config.from_object(__name__)

# Hacky way to allow the secrets import when migrating and
# running the app. *Probably* should be changed
try:
    with open('./h1b/secrets') as f:
        lines = f.read().splitlines()
except:
    with open('./secrets') as f:
        lines = f.read().splitlines()

# Read in the secret values and pass them to the app config dictionary
# to allow connection to the database
keys = dict([line.split('::::') for line in lines if line[0] != '#'])

h1bdb_uri = 'postgresql+psycopg2://{}:{}@{}:5432/h1bdb'.format(
    keys['H1BDB_USERNAME'],
    keys['H1BDB_PASSWORD'],
    keys['H1BDB_HOST'])

app.config['SQLALCHEMY_DATABASE_URI'] = h1bdb_uri
db.init_app(app)

app.config['DEBUG'] = True  # Disable in production
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

if __name__ == '__main__':
    app.run()
