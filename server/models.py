from flask_mongoengine import MongoEngine
from wtforms import Form, fields as wtf
import datetime

db = MongoEngine()


class Role(db.Document):
	name = db.StringField()
	permissions = db.ListField()


class User(db.Document):
	name = db.StringField()
	email = db.EmailField()
	password = db.StringField()
	role = db.ReferenceField(Role)
	created_at = db.DateTimeField(default=datetime.datetime.now)

	def is_active(self):
		return True

	def is_authenticated(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return self.id if self.id else None


class LoginForm(Form):
	email = wtf.StringField('Email')
	password = wtf.StringField('Password')


class RegisterForm(Form):
	name = wtf.StringField('Full Name')
	email = wtf.StringField('Email')
	password = wtf.StringField('Password')
	

class Page(db.Document):
	name = db.StringField()
	path = db.StringField()
	properties = db.DictField()
	
	
class Partial(db.Document):
	name = db.StringField()
	path = db.StringField()
	

class Plugin(db.Document):
	name = db.StringField()
	data = db.DictField()
	
	
class Item(db.Document):
	author = db.ReferenceField(User)
	page = db.ReferenceField(Page)
	partial = db.ReferenceField(Partial)
	data = db.DictField()
	type = db.StringField
	
	def __init__(self, file=None, **kwargs):
		super().__init__(**kwargs)
		self.file = file

	def item(self, item_name, id):
		"""
		Fetches item object from the database, and returns
		the appropriate
		:param item:
		:param id:
		:return:
		"""
		dct = {}
		if isinstance(id, int):
			dct['id'] = str(id)
		elif isinstance(id, str):
			dct['slug'] = id
		obj = Item(**dct)
		if obj.page is not None:
			item_name = Page(obj.page).path
		return item_name+'.html', {'item': obj}


	def items(self, items_name, page=1, per_page=10):
		"""
		Fetches a set of items from the database
		:param items_name:
		:return:
		"""
		html = ''
		item_name = items_name[:-1]
		items = Item.objects.paginate(page=page, per_page=per_page).iter_pages()
		template = open(self.file.name(item_name+'.html', True), 'r').read()
		for item in items:
			html += template.format(item=item)
		if html == '':
			html = 'No '+items_name+' found!'
		return items_name+'.html', {'items': html}