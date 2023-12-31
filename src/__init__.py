from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_qrcode import QRcode
from flask_caching import Cache

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['CACHE_TYPE'] = 'simple'  # Use a simple in-memory cache
app.config['CACHE_DEFAULT_TIMEOUT'] = 300  # Cache timeout (in seconds)

QRcode(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
cache = Cache(app)
login_manager = LoginManager(app)

login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from src import model

with app.app_context():
    db.create_all()

migrate = Migrate(app, db)


from src import routes
