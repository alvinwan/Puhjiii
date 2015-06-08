from server.auth.models import User
from server.plugins.mold.models import Mold
from server import db


class Item(db.Document):
	mold = db.ReferenceField(Mold)
	author = db.ReferenceField(User)
	info = db.DictField()