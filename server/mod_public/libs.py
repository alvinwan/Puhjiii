import config
from flask import render_template
from server.mod_public import models
from server.libs import Puhjee
from wtforms import fields as wtf
from bson import ObjectId

from os.path import join
from bs4 import BeautifulSoup, element


class Item(Puhjee):

	@staticmethod
	def item(item_name, item_id=None, item_slug=None):
		"""
		Fetches item object from the database, and returns
		the appropriate
		:param item_name:
		:param item_id:
		:return:
		"""
		dct = {}
		if item_id:
			dct['id'] = ObjectId(item_id)
		elif item_slug:
			dct['slug'] = item_slug
		obj = Item(**dct).get()
		if hasattr(obj, 'page'):
			item_name = URL(obj.page).path
		return item_name+'.html', {item_name: obj}
	
	@staticmethod
	def items(item_name, type=None, template='public/{items_name}.html',
		page=1, per_page=10, raw=False):
		"""
		Fetches a set of items from the database
		:param item_name:
		:return:
		"""
		items_name = item_name + 's'
		type = type or models.Type.objects(name=item_name).first()
		if not type:
			return template, {'items': 'No such item'}
		items = models.Item.objects(type=ObjectId(type.id)).paginate(page=page, per_page=per_page).items
		if raw:
			return items
		html = ''
		template = template.format(**locals())
		for item in items:
			html += render_template(template, item=item)
		if html == '':
			html = 'No '+item_name+' found!'
		return template, {'items': html}

		
class Type(Puhjee):
	
	@staticmethod
	def types():
		types = []
		for type in models.Type.objects.all():
			types.append(type)
		return types

	def add_fields(self, info):
		fields = {}
		for k in info.split(','):
			if ':' in k:
				k, v = [s.strip() for s in k.split(':')]
				if not hasattr(wtf, v):
					raise UserWarning('No such field')
				fields[k] = v
			else:
				fields[k.strip()] = 'StringField'
		self.info = fields
		return self
	
	def str_fields(self):
		fields = []
		for k, v in getattr(self, 'info', {}).items():
			if v == 'StringField':
				v = ''
			else:
				v = ': '+v
			fields.append(k+v)
		self.info = ', '.join(fields)
		return self
	
	
class URL(Puhjee):
	
	@staticmethod
	def parse(path):
		abs_path = join(config.BASE_DIR, 'server/templates/public', path)
		html = open(abs_path).read()
		soup = BeautifulSoup(html)
		fields = {}
		URL.dfs(soup, fields, 0, 0)
		return fields
		
		
	@staticmethod
	def dfs(soup, fields, depth, i):

		if isinstance(soup, element.NavigableString):
			if hasattr(soup, 'text') and len(soup.text) > 0:
				key = 'd%di%d' % (depth, i)
				fields[key] = soup.text
				soup.text = key
		else:
			for i, child in enumerate(soup.children):
				URL.dfs(child, fields, depth + 1, i)