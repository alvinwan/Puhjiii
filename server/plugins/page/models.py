from server import db


class Page(db.Document):
	title = db.StringField()
	template = db.StringField()
	url = db.StringField(unique=True)
	info = db.DictField()