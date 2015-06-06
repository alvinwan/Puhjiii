from server import db
import datetime


class Role(db.Document):
	name = db.StringField()
	permissions = db.ListField()


class User(db.Document):
	name = db.StringField()
	email = db.EmailField(required=True, unique=True)
	password = db.StringField()
	role = db.ReferenceField(Role)
	created_at = db.DateTimeField(default=datetime.datetime.now)
	is_suspended = db.BooleanField(default=False)