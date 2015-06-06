from server import db
from server.mod_auth.models import User
from server.mod_nest.models import Type


class URL(db.Document):
	title = db.StringField()
	template = db.StringField()
	url = db.StringField(unique=True)
	info = db.DictField()


class Item(db.Document):
	type = db.ReferenceField(Type)
	author = db.ReferenceField(User)
	info = db.DictField()