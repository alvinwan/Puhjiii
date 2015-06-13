from server.auth.models import User
from server.plugins.mold.models import Mold
from server.auth.models import Document
from server import db


class Item(Document):
	mold = db.ReferenceField(Mold)
	author = db.ReferenceField(User)
	info = db.DictField()