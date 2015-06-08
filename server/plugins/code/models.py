from server import db


class Template(db.Document):
	name = db.StringField()
	path = db.StringField()
	defaults = db.DictField()