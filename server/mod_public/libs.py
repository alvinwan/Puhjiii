from flask import render_template
from server.mod_public import models
from server.libs import Puhjee

class Page(Puhjee):
	pass


class Item(Puhjee):

	@staticmethod
	def item(item_name, id):
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
	
	@staticmethod
	def items(items_name, page=1, per_page=10):
		"""
		Fetches a set of items from the database
		:param items_name:
		:return:
		"""
		html = ''
		item_name = items_name[:-1]
		items = models.Item.objects.paginate(page=page, per_page=per_page).iter_pages()
		for item in items:
			html += render_template('public/%s.html' % item_name, item=item)
		if html == '':
			html = 'No '+items_name+' found!'
		return items_name+'.html', {'items': html}