from . import *
from .libs import Item

def process(data):
	type, item_type = data.type, data.item_type
	items = Item.items(item_type, type=type, raw=True)
	for item in items:
		item.href = '/nest/item/%s/%s' % (item_type, str(item.id))
	return dict(type=item_type, items=items)