from server import db
from server.mod_auth.models import User


class Page(db.Document):
	name = db.StringField()
	path = db.StringField()
	properties = db.DictField()


class Partial(db.Document):
	name = db.StringField()
	path = db.StringField()


class Item(db.Document):
	author = db.ReferenceField(User)
	page = db.ReferenceField(Page)
	partial = db.ReferenceField(Partial)
	data = db.DictField()
	type = db.StringField