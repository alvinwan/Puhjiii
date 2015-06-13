from server.auth.models import Document
from server import db


class Plugin(Document):
	name = db.StringField()
	is_active = db.BooleanField()