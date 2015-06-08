from server import db


class Mold(db.Document):
	name = db.StringField(unique=True)
	info = db.DictField()
	page = db.StringField()
	template = db.StringField()
	partial = db.StringField()