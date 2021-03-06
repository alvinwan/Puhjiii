from flask import render_template
from server.libs import Puhjiii
from server.plugins.mold.libs import Mold
from server.plugins.page.libs import Page
from . import models
from bson import ObjectId


class Item(Puhjiii):
	
	model = models.Item

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
			item_name = Page(obj.page).path
		return item_name+'.html', {item_name: obj}

	@staticmethod
	def items(item_name, mold=None, template='public/{items_name}.html',
	          page=1, per_page=10, raw=False):
		"""
		Fetches a set of items from the database
		:param item_name:
		:return:
		"""
		items_name = item_name + 's'
		mold = mold or Mold.model.objects(name=item_name).first()
		if not mold:
			return template, {'items': 'No such item'}
		items = Item.model.objects(mold=ObjectId(mold.id)).paginate(page=page, per_page=per_page).items
		if raw:
			return items
		html = ''
		template = template.format(**locals())
		for item in items:
			html += render_template(template, item=item)
		if html == '':
			html = 'No '+item_name+' found!'
		return template, {'items': html}