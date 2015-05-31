import flask

from flask.ext.mongoengine import MongoEngine
from flask.ext.login import LoginManager

app = flask.Flask(__name__)
app.config.from_object(__name__)
app.config['MONGODB_SETTINGS'] = {'DB': 'puhjee'}
app.config['TESTING'] = True
app.config['SECRET_KEY'] = 'flask+mongoengine=<3'

db = MongoEngine()
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

import server.views