from flask import Flask
from flask_mongoengine import MongoEngine
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

import config

# Create and name app
app = Flask(__name__)

# database connection
app.config['MONGODB_SETTINGS'] = {'DB': config.DB}
app.config['SECRET_KEY'] = config.SECRET_KEY
app.debug = config.DEBUG

# initialize MongoEngine with app
db = MongoEngine()
db.init_app(app)

# initialize Flask-Login with app
login_manager = LoginManager()
login_manager.init_app(app)

# initialize encryption mechanism
bcrypt = Bcrypt(app)

from server.auth.views import mod_auth
from server.nest.views import mod_nest
from server.public.views import mod_public
from server.nest.libs import Plugin

Plugin.load_views()

# Register blueprints
app.register_blueprint(mod_auth)
app.register_blueprint(mod_nest)
app.register_blueprint(mod_public)