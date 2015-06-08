from server import db


class Plugin(db.Document):
	name = db.StringField()
	is_active = db.BooleanField()