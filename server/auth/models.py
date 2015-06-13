from server import db
import datetime


class Document(db.Document):
	created_at = db.DateTimeField(default=datetime.datetime.now)
	updated_at = db.DateTimeField(default=datetime.datetime.now)
	
	meta = {
		'abstract': True
	}


class Role(Document):
	name = db.StringField()
	permissions = db.ListField()


class User(Document):
	name = db.StringField()
	email = db.EmailField(required=True, unique=True)
	password = db.StringField()
	role = db.ReferenceField(Role)
	created_at = db.DateTimeField(default=datetime.datetime.now)
	is_suspended = db.BooleanField(default=False)