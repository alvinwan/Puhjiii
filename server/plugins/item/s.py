"""

Types

Displays all items types

@author: Alvin Wan
"""

from server.mod_public.libs import Item

path = 'item'
templates = ['partials/items.html']


def process(data):
	type, item_type = data.type, data.item_type
	items = Item.items(item_type, type=type, raw=True)
	for item in items:
		item.href = '/nest/item/%s/%s' % (item_type, str(item.id))
	return dict(type=item_type, items=items)