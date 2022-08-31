from flask import Flask, render_template
import dateutil.parser
import babel
from flask_migrate import Migrate
from config import SQLALCHEMY_DATABASE_URI
from flask_sqlalchemy import SQLAlchemy
import os
from router.route_venues import path1
from router.route_artists import path2
from router.route_shows import path3
# from config import Config

#----------------------------------------------------------------------------#
# Set-up flask app
#----------------------------------------------------.------------------------#

app = Flask(__name__)
# moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# connects to a local postgresql database
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Set-up database connection with psycopg2
#----------------------------------------------------------------------------#


app.register_blueprint(path1, url_prefix = '/venues')
app.register_blueprint(path2, url_prefix = '/artists')
app.register_blueprint(path3, url_prefix = '/shows')


@app.route('/')
def index():
    return render_template('pages/home.html')

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True,host='0.0.0.0', port=port)