from server.auth.models import Document
from server import db


class Mold(Document):
	name = db.StringField(unique=True)
	info = db.DictField()
	page = db.StringField()
	template = db.StringField()
	partial = db.StringField()