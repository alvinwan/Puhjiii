from server.auth.models import Document
from server import db


class Template(Document):
	name = db.StringField()
	path = db.StringField()
	defaults = db.DictField()