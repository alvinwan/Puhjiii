from server import db


class Plugin(db.Document):
	name = db.StringField()
	is_active = db.BooleanField()


class Type(db.Document):
	name = db.StringField(unique=True)
	info = db.DictField()
	page = db.StringField()
	template = db.StringField()
	partial = db.StringField()