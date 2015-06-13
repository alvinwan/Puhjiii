from server.auth.models import Document
from server import db


class Page(Document):
	title = db.StringField(unique=True)
	template = db.StringField()
	url = db.StringField(unique=True)
	info = db.DictField()