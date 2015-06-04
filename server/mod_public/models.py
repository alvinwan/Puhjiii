from server import db
from server.mod_auth.models import User


class URL(db.Document):
	title = db.StringField()
	template = db.StringField()
	url = db.StringField(unique=True)
	info = db.DictField()


class Type(db.Document):
	name = db.StringField(unique=True)
	info = db.DictField()
	page = db.StringField()
	template = db.StringField()
	partial = db.StringField()


class Item(db.Document):
	type = db.ReferenceField(Type)
	author = db.ReferenceField(User)
	info = db.DictField()