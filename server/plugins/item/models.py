from server.auth.models import User
from server.plugins.type.models import Type
from server import db


class Item(db.Document):
	type = db.ReferenceField(Type)
	author = db.ReferenceField(User)
	info = db.DictField()